#!/usr/bin/env python

# Copyright 2016 Tan N. Le
# lenhattan86@gmail.com
# kubectl delete pods --grace-period=0 --force job-vgg16-gpu-19-12-128-0
import argparse
import json
import sys
import urllib2
import csv
import subprocess
import os
import datetime
from time import time
from time import sleep
import sched
from threading import Timer
import threading
from threading import Thread

from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *
from job_info import *

print ("python automation_tool.py --test=False")
parser = argparse.ArgumentParser()
parser.add_argument('--test', help='True or False', required=False, default="True")
parser.add_argument('--measure', help='True or False', required=False, default="False")
parser.add_argument('--interval', help='Polling interval  (secs)', required=False, default="1")
parser.add_argument('--profiling', help='profiling True/False', required=False, default="True")
parser.add_argument('--workload', help='workload folder', required=False, default="traces/small")
parser.add_argument('--nusers', help='number of users', required=False, default="2")
parser.add_argument('--measuresec', help='number of users', required=False, default="False")
parser.add_argument('--folder', help='output folder', required=False, default="automation_tool")

args = vars(parser.parse_args())
IS_TEST    = bool(args['test']=="True")
IS_MEASURE = bool(args['measure']=="True")
interval = float(args['interval'])
isProfiling = bool(args['profiling']=="True")
workload = args['workload']
nusers = int(args['nusers'])
IS_MEASURE_SEC=bool(args['measuresec']=="True")
FOLDER=args['folder']

jobSubmissionLock = threading.Lock()

IS_DEBUG = True

if IS_TEST:
    print("please indicate --test=False")
    endTime = 2*interval


IS_MY_SCHEDULER = True
if IS_MEASURE_SEC:
    IS_MY_SCHEDULER = False
    IS_MEASURE = True

GPU_PREFIX = "g-"
PROFILING_PREFIX = "profiling"
numBatch1Percent_CPU = 0.0/100
numBatch2Percent_CPU = 1.0/100
numBatch1Percent_GPU = 0.0/100
numBatch2Percent_GPU = 1.0/100
# numBatch2 = 200

GI = 1024*1024*1024
SCHEDULER = "kube-scheduler"
MY_SCHEDULER = "my-scheduler"
DEFAULT_NS = "default"

MAX_CPU = 19
MAX_GPU = 1
MAX_MEM = 12
cpu=19
mem=12
gpuCpu=1
gpu=1
gpuMem=2

if IS_TEST:
    nusers=1
    userStrArray = ["user1"]

def log(str):
    if (IS_DEBUG):
        print(str)

def listJobStatus():
    startedPods   = []
    completedPods = []
    pendingJobs = []
    # p = subprocess.Popen(["kubectl get pods --all-namespaces --field-selector=status.phase!=Pending"], 
    p = subprocess.Popen(["kubectl get pods --all-namespaces"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    if IS_TEST:
        output = """NAMESPACE     NAME                                       READY     STATUS      RESTARTS   AGE
user1       user1-profiling-cpu1-1                          0/1       Running   0          19h
user1       user1-profiling-cpu1-1                          0/1       Completed   0          19h
user1       user1-profiling-cpu2-1                        0/1       Running   0          19h
user1       user1-profiling-cpu2-1                          0/1       Completed   0          19h
user1       user1-profiling-gpu1-1                          0/1       Running   0          19h
user1       user1-profiling-gpu1-1                          0/1       Completed   0          19h
user1       user1-profiling-gpu2-1                          0/1       Running   0          19h
user1       user1-profiling-gpu2-1                          0/1       Completed   0          19h
user1       user1-1                          0/1      Running   0          19h
user1       user1-1                          0/1      Completed   0          19h
user1       g-user1-1                          0/1      Running   0          19h
user1       g-user1-1                          0/1      Completed   0          19h
"""
#         output = """NAME      READY     STATUS    RESTARTS   AGE
# job-1     0/1       Pending   0          1m 
# """
        p_status=0    

    # completedJobs = 0
    # time_step = time_step + interval
    if p_status != 0:        
        print('Could not access the kubernetes')
    else:
        lines=output.split("\n")            
        for line in lines[1:len(lines)-1]:            
            strArr=line.split()            
            user=strArr[0]
            if user == "kube-system":
                continue
            mPodName=strArr[1]
            podStatus=strArr[3]
            if user != "kube-system":
                if podStatus == "Pending":
                    pendingJobs.append(mPodName)                    
                if podStatus == "Completed":
                    completedPods.append(mPodName)
                if podStatus == "ContainerCreating" or podStatus == "Running":
                # if podStatus == "Running":
                    startedPods.append(mPodName)                
                    
    currTime = time()
    return pendingJobs, startedPods, completedPods, currTime

def updateJobInfo(startedJobs, completedJobs, mJobs, currTime):    
    for sJob in startedJobs:
        # get jobId from jobName
        temp = sJob.split("-")
        jobIdKey = temp[len(temp)-1]
        if mJobs.get(jobIdKey) is not None and mJobs.get(jobIdKey).jobName == sJob:
            if mJobs[jobIdKey].starTime < 0:
                mJobs[jobIdKey].starTime = currTime

    for sJob in completedJobs:
        # get jobId from jobName
        temp = sJob.split("-")
        jobIdKey = temp[len(temp)-1]
        if mJobs.get(jobIdKey) is not None and mJobs.get(jobIdKey).jobName == sJob:
            if mJobs[jobIdKey].complTime < 0:
                mJobs[jobIdKey].endTime = currTime    
                if mJobs[jobIdKey].starTime < 0:
                    log("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative. (this job is too short)")
                    mJobs[jobIdKey].starTime = currTime-(interval/2) # This job finishes shorter than a interval
                mJobs[jobIdKey].complTime = mJobs[jobIdKey].endTime - mJobs[jobIdKey].starTime
                log("[INFO] " + mJobs[jobIdKey].jobName + "'s compl. time is "+ str(mJobs[jobIdKey].complTime ))

def updateFullJobInfo(startedJobs, completedJobs, mJobs, currTime, isCPU):    
    if isCPU:
        for sJob in startedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[len(temp)-1]
            if mJobs.get(jobIdKey) is not None and (mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].starTime < 0:
                    mJobs[jobIdKey].starTime = currTime

        for sJob in completedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[len(temp)-1]
            if mJobs.get(jobIdKey) is not None and (mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].complTime < 0:
                    mJobs[jobIdKey].endTime = currTime    
                    if mJobs[jobIdKey].starTime < 0:
                        log("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative.")                    
                    mJobs[jobIdKey].complTime = mJobs[jobIdKey].endTime - mJobs[jobIdKey].starTime
                    log("[INFO] " + mJobs[jobIdKey].jobName + "'s compl. time is "+ str(mJobs[jobIdKey].complTime ))
    else:
        for sJob in startedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[len(temp)-1]
            if mJobs.get(jobIdKey) is not None and (GPU_PREFIX + mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].starTimeGpu < 0:
                    mJobs[jobIdKey].starTimeGpu = currTime

        for sJob in completedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[len(temp)-1]
            if mJobs.get(jobIdKey) is not None and (GPU_PREFIX + mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].complTimeGpu < 0:
                    mJobs[jobIdKey].endTimeGpu = currTime    
                    if mJobs[jobIdKey].starTimeGpu < 0:
                        log("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative.")                    
                    mJobs[jobIdKey].complTimeGpu = mJobs[jobIdKey].endTimeGpu - mJobs[jobIdKey].starTimeGpu
                    log("[INFO] " + mJobs[jobIdKey].jobName + "'s GPU compl. time is "+ str(mJobs[jobIdKey].complTimeGpu ))

    for keyId in mJobs:   
        if (mJobs.get(keyId) is not None):
            if  mJobs[keyId].complTime >= 0 and mJobs[keyId].complTimeGpu >= 0 and (not mJobs[keyId].isComputed):
                if mJobs[keyId].complTimeGpu == 0:
                    mJobs[keyId].complTimeGpu = 0.0001
                mJobs[keyId].speedup = mJobs[keyId].complTime / mJobs[keyId].complTimeGpu
                log("[INFO] " + mJobs[keyId].jobName + "'s speedup is "+ str(mJobs[keyId].speedup))
                mJobs[keyId].isComputed = True

def estimateComplTime(fJobs, sJobs1, sJobs2, isCPU):
    for keyId in fJobs:
        if isCPU:
            if (fJobs.get(keyId) is not None) and fJobs[keyId].estComplTimeCpu < 0:
                if (sJobs1.get(keyId) is not None) and (sJobs2.get(keyId) is not None):
                    if (sJobs1.get(keyId).complTime >= 0) and (sJobs2.get(keyId).complTime >= 0):
                        # linear model a * (numberofbatches) + b
                        a = (sJobs1[keyId].complTime - sJobs2[keyId].complTime) / (sJobs1[keyId].numBatches - sJobs2[keyId].numBatches)
                        b = sJobs1[keyId].complTime - a*sJobs1[keyId].numBatches                        
                        fJobs[keyId].estComplTimeCpu = a*fJobs[keyId].numBatches + b
                        if fJobs[keyId].estComplTimeCpu < 0 or sJobs2[keyId].complTime < sJobs1[keyId].complTime:
                            fJobs[keyId].estComplTimeCpu = max(sJobs2[keyId].complTime, sJobs1[keyId].complTime)
                            fJobs[keyId].estComplTimeCpu = max((100/numBatch2Percent_CPU) * interval, fJobs[keyId].estComplTimeCpu )
                            log("[ERROR] " + fJobs.get(keyId).jobName +" is TOO SHORT on CPU ")  
                        log("[INFO] " + fJobs.get(keyId).jobName +"'s estimated compl. time on CPU is " + str(fJobs[keyId].estComplTimeCpu))

                    
        else:
            if (fJobs.get(keyId) is not None) and fJobs[keyId].estComplTimeGpu < 0:
                if (sJobs1.get(keyId) is not None) and (sJobs2.get(keyId) is not None):
                    if (sJobs1.get(keyId).complTime >= 0) and (sJobs2.get(keyId).complTime >= 0):
                        # linear model a * (numberofbatches) + b
                        a = (sJobs1[keyId].complTime - sJobs2[keyId].complTime) / (sJobs1[keyId].numBatches - sJobs2[keyId].numBatches)
                        b = sJobs1[keyId].complTime - a*sJobs1[keyId].numBatches
                        fJobs[keyId].estComplTimeGpu = a*fJobs[keyId].numBatches2 + b
                        if fJobs[keyId].estComplTimeGpu < 0 or sJobs2[keyId].complTime < sJobs1[keyId].complTime:
                            fJobs[keyId].estComplTimeGpu = max(sJobs2[keyId].complTime, sJobs1[keyId].complTime)
                            fJobs[keyId].estComplTimeGpu = max((100/numBatch2Percent_CPU) * interval,fJobs[keyId].estComplTimeGpu)
                            log("[ERROR] " + fJobs.get(keyId).jobName +" is TOO SHORT on GPU ")
                        log("[INFO] " + fJobs.get(keyId).jobName +"'s estimated compl. time on GPU is " + str(fJobs[keyId].estComplTimeGpu))

        # if  fJobs[keyId].estComplTimeCpu >= 0 and fJobs[keyId].estComplTimeGpu >= 0 and (not fJobs[keyId].isEstimated) : 
        #     if fJobs[keyId].estComplTimeGpu == 0:
        #         fJobs[keyId].estComplTimeGpu = 0.0001
        #     fJobs[keyId].estSpeedup = fJobs[keyId].estComplTimeCpu / fJobs[keyId].estComplTimeGpu
        #     log("[INFO] " + fJobs[keyId].jobName + "'s estimated speedup is "+ str(fJobs[keyId].estSpeedup))
        #     fJobs[keyId].isEstimated = True

def estimateSpeedup(fJobs, cJobs, gJobs):
    for keyId in fJobs:    
        if (fJobs.get(keyId) is not None) and (not fJobs[keyId].isEstimated):
            if (cJobs.get(keyId) is not None) and (gJobs.get(keyId) is not None):
                if (cJobs.get(keyId).complTime >= 0) and (gJobs.get(keyId).complTime >= 0):
                    # linear model a * (numberofbatches) + b
                    if gJobs[keyId].complTime == 0:
                        gJobs[keyId].complTime = 0.00001
                    fJobs[keyId].estSpeedup = cJobs[keyId].complTime / gJobs[keyId].complTime
                    log("[INFO] " + fJobs[keyId].jobName + "'s estimated speedup is "+ str(fJobs[keyId].estSpeedup))
                    fJobs[keyId].isEstimated = True
                            

def submitJob(podName, job_folder, yamfile, username):
    log("[INFO] Submit job " + podName + " on CPU: " + " on GPU: ")
    # deleteJob(podName, username)
    p = subprocess.Popen(["kubectl create -f  " + job_folder + '/' + yamfile+ ".yaml -n " + username ],
            stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait()

def deleteJob(podName, username):
    p = subprocess.Popen(["kubectl delete pods "+podName +" -n " + username], 
            stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()   
    p_status = p.wait()

def deleteAllJobs(username):
    p = subprocess.Popen(["kubectl delete pods --all -n" + username +"  --grace-period=0 --force "], 
            stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()   
    p_status = p.wait()    

def createSubCommands(cmd, numbatches, isCPU):
    tempArray = cmd.split("--num_batches=")
    if len(tempArray) == 2:       
        if isCPU:
            # b1 = int(numbatches*numBatch1Percent_CPU)
            # b2 = int(numbatches*numBatch1Percent_CPU)
            # if b1 <= 10: # prevent unknown pod error
            #     b1 = b1 + 10
            #     b2 = b2 + 10
            subCmd1 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch1Percent_CPU))
            subCmd2 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch2Percent_CPU))
        else:
            subCmd1 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch1Percent_GPU))
            subCmd2 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch2Percent_GPU))
    else:
        log("[ERROR] command shoud have --num_batches= at the end")

    return subCmd1, subCmd2

def writeJobsToCsv(jobs, filename):
    rows=[]
    for jobKey in jobs:
        jobInfo = jobs[jobKey]
        row = [jobKey, jobInfo.jobName , jobInfo.userName, jobInfo.estComplTimeCpu, jobInfo.estComplTimeGpu, 
            jobInfo.complTime, jobInfo.complTimeGpu, jobInfo.estSpeedup, jobInfo.speedup, jobInfo.isGpuJob] 
        rows.append(row) 

    ofile  = open(job_folder + '/' + filename + '.csv', "wb")
    writer = csv.writer(ofile, dialect='excel')
    writer.writerows(rows) 

def createYamlFile(activeJob, prefix, yamfile, isGPU, isScheduled):
    f_yaml = open(job_folder + '/' + yamfile+ ".yaml",'w')   
    if isScheduled:
        f_yaml.write(strPodYaml(prefix, activeJob, MY_SCHEDULER, isGPU))
    else:
        f_yaml.write(strPodYaml(prefix, activeJob, SCHEDULER, isGPU))
    f_yaml.close()    

start_time = time()
## only submit jobs if they are estimated.
def isAllJobsReady(fJobs):
    for jobKey in fJobs:
        # if fJobs[jobKey].estComplTimeCpu <0 or fJobs[jobKey].estComplTimeGpu <0:
        #     return False
        if fJobs[jobKey].estComplTimeCpu <0:
            return False  

    elapsed_time = time() - start_time
    log("[INFO] Profiling lasts " + str(elapsed_time) + " seconds")
    return True

def isAllSubmitted(fJobs):
    nSubmittedJobs = 0
    for jobKey in fJobs:
        jobInfo = fJobs[jobKey]
        if jobInfo.isSubmitted: 
            nSubmittedJobs=nSubmittedJobs+1

    return nSubmittedJobs >= len(fJobs)

def submitFullJobs(fJobs):
    # deletedKeys = []
    nSubmittedJobs = 0
    for jobKey in fJobs:
        # if fJobs[jobKey].isEstimated:
        # if fJobs[jobKey].estComplTimeCpu >=0 and fJobs[jobKey].estComplTimeGpu >=0:
        if isAllJobsReady(fJobs) or (not isProfiling):
            jobInfo = fJobs[jobKey]
            if not jobInfo.isSubmitted:                
                job = jobInfo.job            
                cpuCmd = job.cpuProfile.jobCmd
                gpuCmd = job.gpuProfile.jobCmd

                cpu_usage = Resource(job.cpuProfile.demand.MilliCPU,job.cpuProfile.demand.Memory, job.cpuProfile.demand.NvidiaGPU)
                gpu_usage = Resource(job.gpuProfile.demand.MilliCPU, job.gpuProfile.demand.Memory, job.gpuProfile.demand.NvidiaGPU)
                
                if (isProfiling):
                    activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobKey, cpuCmd, gpuCmd, jobInfo.estComplTimeCpu, jobInfo.estComplTimeGpu)
                else:
                    activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobKey, cpuCmd, gpuCmd, job.cpuProfile.compl, job.gpuProfile.compl)

                prefix = jobInfo.userName
                yamfile = jobInfo.jobName
                createYamlFile(activeJob, prefix, yamfile, False, IS_MY_SCHEDULER) 

                log("[INFO] Submit job " +jobInfo.userName +"/" + jobInfo.jobName)
                submitJob(jobInfo.jobName, job_folder, yamfile, jobInfo.userName) 
                jobInfo.isSubmitted=True
            else:
                nSubmittedJobs = nSubmittedJobs + 1
            # deletedKeys.append(jobKey)

        if IS_MEASURE_SEC:
            if isAllJobsReady(fJobs)  or (not isProfiling):    
                jobInfo = fJobs[jobKey]
                if not jobInfo.isSubmittedGpu:
                    job = jobInfo.job
                    cpuCmd = job.cpuProfile.jobCmd
                    gpuCmd = job.gpuProfile.jobCmd

                    cpu_usage = Resource(job.cpuProfile.demand.MilliCPU,job.cpuProfile.demand.Memory, job.cpuProfile.demand.NvidiaGPU)
                    gpu_usage = Resource(job.gpuProfile.demand.MilliCPU, job.gpuProfile.demand.Memory, job.gpuProfile.demand.NvidiaGPU)
                    activeJob = ActiveJob(gpu_usage,cpu_usage,  0, 0, jobKey, gpuCmd, cpuCmd, 0, 0)                    
                    prefix = GPU_PREFIX + jobInfo.userName
                    yamfile = GPU_PREFIX + jobInfo.jobName
                    createYamlFile(activeJob, prefix, yamfile, True, IS_MY_SCHEDULER)            
                    submitJob(yamfile, job_folder, yamfile, jobInfo.userName) 
                    jobInfo.isSubmittedGpu=True

    if nSubmittedJobs >= len(fJobs):
        return True

    return False

this_path = os.path.dirname(os.path.realpath(__file__))
job_folder = this_path + "/" + FOLDER 
#shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
#os.mkdir(job_folder)    

################################### MAIN Script ###############################################

print "====== AUTOMATION-TOOL ====="
def main():
    ## initialization   
    print "====== main() ====="
    start_time = time()
    # your code
    
    users = []
    fullJobs = {}
    cpuShortJobs_1 = {}
    cpuShortJobs_2 = {}
    gpuShortJobs_1 = {}
    gpuShortJobs_2 = {}
    userStrArray=[]
    for i in range(nusers):
        print('user'+str(i+1))
        userStrArray.append("user"+str(i+1))   

    # read jobs from files to jobs
    for i in range(len(userStrArray)):
        strUser=userStrArray[i]
        # log("read " + strUser)
        jobs    = readJobRR(this_path+"/"+workload, strUser+".txt", i-1, len(userStrArray))
        newUser = User(strUser, jobs)
        # log(newUser.toString())
        users.append(newUser)
        # create user name space
        f = open(job_folder + '/' + newUser.username + ".yaml",'w')
        f.write(strUserYaml(newUser.username))
        f.close()
        log("kubectl create -f  " + job_folder + '/' + newUser.username+ ".yaml" )
        p = subprocess.Popen(["kubectl create -f  " + job_folder + '/' + newUser.username+ ".yaml" ],
                stdout=subprocess.PIPE, shell=True)                   
        (output, err) = p.communicate()    
        p_status = p.wait()

    # create profiling jobs
    jobId = 0
    deleteAllJobs(DEFAULT_NS)
    for user in users:
        deleteAllJobs(user.username)
        # create jobs        
        for job in user.jobs:
            jobId = jobId + 1
            jobIdKey = str(jobId)
            
            jobName = user.username + "-" + str(jobId)
            fullJobs[jobIdKey]  = JobInfo(jobId, jobName, user.username, job.numBatches, job.numBatches2)
            fullJobs[jobIdKey].job = job
            # deleteJob(jobName, user.username)
            
            if (isProfiling):
                # read the number of batch from the job
                cpuCmd = job.cpuProfile.jobCmd
                gpuCmd = job.gpuProfile.jobCmd
                cpuCmd1, cpuCmd2 = createSubCommands(cpuCmd, job.numBatches, True)        
                gpuCmd1, gpuCmd2 = createSubCommands(gpuCmd, job.numBatches2, False)

                # for the small number of batches
                cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
                gpu_usage = Resource(1*MILLI, gpuMem *GI, gpu)

                # prepare jobs for CPU     
                prefix = PROFILING_PREFIX + "-cpu1"
                jobName = str(user.username) +"-"+ prefix
                yamfile = jobName + "-" + str(jobId)
                numBatch1 = job.numBatches * numBatch1Percent_CPU
                newJob = JobInfo(jobId, yamfile, user.username, numBatch1, 0)
                activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId, cpuCmd1, gpuCmd, 0, 0)
                createYamlFile(activeJob, jobName, yamfile, False, IS_MY_SCHEDULER)
                # submitJob(yamfile, job_folder, yamfile, DEFAULT_NS)     
                thread1 = Thread(target = submitJob, args = (yamfile, job_folder, yamfile, DEFAULT_NS))   
                thread1.start()    
                cpuShortJobs_1[jobIdKey] = newJob

                ###################################################################
                # pendingJobs, startedJobs, completedJobs, currTime = listJobStatus()
                # updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                ###################################################################

                prefix = PROFILING_PREFIX + "-cpu2"
                jobName = str(user.username)  +"-"+ prefix
                yamfile = jobName + "-" + str(jobId)
                numBatch2 = job.numBatches * numBatch2Percent_CPU
                newJob  = JobInfo(jobId, yamfile, user.username, numBatch2, 0)
                activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId,  cpuCmd2, gpuCmd2, 0, 0)
                createYamlFile(activeJob, jobName, yamfile, False, IS_MY_SCHEDULER)
                # submitJob(yamfile, job_folder, yamfile, DEFAULT_NS)     
                thread2 = Thread(target = submitJob, args = (yamfile, job_folder, yamfile, DEFAULT_NS))   
                thread2.start()        
                cpuShortJobs_2[jobIdKey] = newJob

                ###################################################################
                # pendingJobs, startedJobs, completedJobs, currTime = listJobStatus()
                # updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                ###################################################################

                # prepare jobs for GPU        
                prefix = PROFILING_PREFIX + "-gpu1"
                jobName = str(user.username) +"-"+ prefix
                yamfile = jobName + "-" + str(jobId)
                numBatch1 = job.numBatches2 * numBatch1Percent_GPU
                newJob = JobInfo(jobId, yamfile, user.username, numBatch1, 0)
                activeJob = ActiveJob(gpu_usage, cpu_usage,  0, 0, jobId, gpuCmd1, cpuCmd1, 1, 0 )
                createYamlFile(activeJob, jobName, yamfile, True, IS_MY_SCHEDULER)
                # submitJob(yamfile, job_folder, yamfile, DEFAULT_NS)     
                thread3 = Thread(target = submitJob, args = (yamfile, job_folder, yamfile, DEFAULT_NS))   
                thread3.start()          
                gpuShortJobs_1[jobIdKey] = newJob

                ###################################################################
                # pendingJobs, startedJobs, completedJobs, currTime = listJobStatus()
                # updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                ###################################################################

                prefix = PROFILING_PREFIX + "-gpu2"
                jobName = str(user.username) +"-"+ prefix
                yamfile = jobName + "-" + str(jobId)
                numBatch2 = job.numBatches2 * numBatch2Percent_GPU
                newJob  = JobInfo(jobId, yamfile, user.username, numBatch2, 0)
                activeJob = ActiveJob(gpu_usage, cpu_usage,  0, 0, jobId, gpuCmd2,  cpuCmd2, 1, 0)
                createYamlFile(activeJob, jobName, yamfile, True, IS_MY_SCHEDULER)
                # submitJob(yamfile, job_folderinterval, yamfile, DEFAULT_NS)     
                thread4 = Thread(target = submitJob, args = (yamfile, job_folder, yamfile, DEFAULT_NS))   
                thread4.start()         
                gpuShortJobs_2[jobIdKey] = newJob 
                
                ###################################################################
                pendingJobs, startedJobs, completedJobs, currTime = listJobStatus()                
                updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
                updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
                updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
                ###################################################################
                thread1.join
                thread2.join
                thread3.join
                thread4.join

                # estimateSpeedup(fullJobs, cpuShortJobs_1, gpuShortJobs_1)
                # estimateSpeedup(fullJobs, gpuShortJobs_1, gpuShortJobs_2, False)

                # submitFullJobs(fullJobs)

                if IS_MEASURE:
                    updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, True)
                if IS_MEASURE_SEC:    
                    updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, False)

    # submitFullJobs(fullJobs)        
    # step 4: measure the job completion time.
    started = False
    rows = []
  
    iTime = 0
    infiniteLoop = True
    # if IS_TEST:
    #     infiniteLoop = True
    while infiniteLoop:
        sleep(interval)

        # TODO: submit jobs when jobs arrive

        pendingJobs, startedJobs, completedJobs, currTime = listJobStatus()
        if (isProfiling):
            updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
            updateJobInfo(startedJobs, completedJobs, cpuShortJobs_2, currTime)
            updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
            updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
        
            # step 5: estimation
            # estimateSpeedup(fullJobs, cpuShortJobs_1, gpuShortJobs_1)
            estimateComplTime(fullJobs, cpuShortJobs_1, cpuShortJobs_2, True)
            estimateComplTime(fullJobs, gpuShortJobs_1, gpuShortJobs_2, False)

        # log("startedJobs: " + str(startedJobs))
        # log("completedJobs: " + str(completedJobs))
        # log("fullJobs: " + fullJobs["1"].jobName)
        if IS_MEASURE:
            updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, True)
        if IS_MEASURE_SEC:    
            updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, False)
            
        # step 6: submit profiled jobs to the system
        # log ("size of full jobs: " + str(len(fullJobs)))
       
        submitFullJobs(fullJobs)

        if (iTime % (interval*30) == 0): # write down every 1 min.
            # step 6: write results out
            writeJobsToCsv(fullJobs,'fullJobs')
            if (isProfiling):
                writeJobsToCsv(cpuShortJobs_1,'cpuShortJobs_1')    
                writeJobsToCsv(gpuShortJobs_1,'gpuShortJobs_1') 
                writeJobsToCsv(cpuShortJobs_2,'cpuShortJobs_2')    
                writeJobsToCsv(gpuShortJobs_2,'gpuShortJobs_2') 
                
        iTime = iTime + interval     
        isExit = isAllSubmitted(fullJobs)
        if (isExit and (not IS_MEASURE)):
            writeJobsToCsv(fullJobs,'fullJobs')
            if (isProfiling):
                writeJobsToCsv(cpuShortJobs_1,'cpuShortJobs_1')    
                writeJobsToCsv(gpuShortJobs_1,'gpuShortJobs_1') 
                writeJobsToCsv(cpuShortJobs_2,'cpuShortJobs_2')    
                writeJobsToCsv(gpuShortJobs_2,'gpuShortJobs_2') 
            elapsed_time = time() - start_time
            log("[INFO] Estimation lasts " + str(elapsed_time) + " seconds")
            log("[INFO] All jobs are submitted ==> Please wait for jobs to be finished")
            break 

if __name__ == "__main__": main()