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

from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *
from job_info import *

parser = argparse.ArgumentParser()
parser.add_argument('--test', help='True or False', required=False, default="True")
args = vars(parser.parse_args())
IS_TEST = bool(args['test']=="True")

interval=1.0
if IS_TEST:
    print("please indicate --test=False")
    endTime = 2*interval

IS_MEASURE = True
GPU_PREFIX = "g-"
def listJobStatus():
    startedPods   = []
    completedPods = []
    # p = subprocess.Popen(["kubectl get pods --all-namespaces --field-selector=status.phase!=Pending"], 
    p = subprocess.Popen(["kubectl get pods --all-namespaces"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    if IS_TEST:
        output = """NAMESPACE     NAME                                       READY     STATUS      RESTARTS   AGE
user1       cpu1-1                          0/1       Running   0          19h
user1       cpu1-1                          0/1       Completed   0          19h
user1       cpu2-1                          0/1       Running   0          19h
user1       cpu2-1                          0/1       Completed   0          19h
user1       gpu1-1                          0/1       Running   0          19h
user1       gpu1-1                          0/1       Completed   0          19h
user1       gpu2-1                          0/1       Running   0          19h
user1       gpu2-1                          0/1       Completed   0          19h
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
        print 'Could not access the kubernetes'
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
                    continue
                if podStatus == "Completed":
                    completedPods.append(mPodName)
                # if podStatus == "ContainerCreating" or podStatus == "Running":
                if podStatus == "Running":
                    startedPods.append(mPodName)
    currTime = time()
    return startedPods, completedPods, currTime

def updateJobInfo(startedJobs, completedJobs, mJobs, currTime):    
    for sJob in startedJobs:
        # get jobId from jobName
        temp = sJob.split("-")
        jobIdKey = temp[1]
        if mJobs.get(jobIdKey) is not None and mJobs.get(jobIdKey).jobName == sJob:
            if mJobs[jobIdKey].starTime < 0:
                mJobs[jobIdKey].starTime = currTime

    for sJob in completedJobs:
        # get jobId from jobName
        temp = sJob.split("-")
        jobIdKey = temp[1]
        if mJobs.get(jobIdKey) is not None and mJobs.get(jobIdKey).jobName == sJob:
            if mJobs[jobIdKey].complTime < 0:
                mJobs[jobIdKey].endTime = currTime    
                if mJobs[jobIdKey].starTime < 0:
                    print("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative.")                    
                mJobs[jobIdKey].complTime = mJobs[jobIdKey].endTime - mJobs[jobIdKey].starTime
                print("[INFO] " + mJobs[jobIdKey].jobName + "'s compl. time is "+ str(mJobs[jobIdKey].complTime ))

def updateFullJobInfo(startedJobs, completedJobs, mJobs, currTime, isCPU):    
    if isCPU:
        for sJob in startedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[1]
            if mJobs.get(jobIdKey) is not None and (mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].starTime < 0:
                    mJobs[jobIdKey].starTime = currTime

        for sJob in completedJobs:
            # get jobId from jobName
            temp = sJob.split("-")
            jobIdKey = temp[1]
            if mJobs.get(jobIdKey) is not None and (mJobs.get(jobIdKey).jobName) == sJob:
                if mJobs[jobIdKey].complTime < 0:
                    mJobs[jobIdKey].endTime = currTime    
                    if mJobs[jobIdKey].starTime < 0:
                        print("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative.")                    
                    mJobs[jobIdKey].complTime = mJobs[jobIdKey].endTime - mJobs[jobIdKey].starTime
                    print("[INFO] " + mJobs[jobIdKey].jobName + "'s compl. time is "+ str(mJobs[jobIdKey].complTime ))
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
                        print("[ERROR] " + mJobs[jobIdKey].jobName + "'s start time is negative.")                    
                    mJobs[jobIdKey].complTimeGpu = mJobs[jobIdKey].endTimeGpu - mJobs[jobIdKey].starTimeGpu
                    print("[INFO] " + mJobs[jobIdKey].jobName + "'s GPU compl. time is "+ str(mJobs[jobIdKey].complTimeGpu ))

    for keyId in mJobs:   
        if (mJobs.get(keyId) is not None):
            if  mJobs[keyId].complTime >= 0 and mJobs[keyId].complTimeGpu >= 0 and (not mJobs[keyId].isComputed):
                if mJobs[keyId].complTimeGpu == 0:
                    mJobs[keyId].complTimeGpu = 0.0001
                mJobs[keyId].speedup = mJobs[keyId].complTime / mJobs[keyId].complTimeGpu
                print("[INFO] " + mJobs[keyId].jobName + "'s speedup is "+ str(mJobs[keyId].speedup))
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
                        print("[INFO] " + fJobs.get(keyId).jobName +"'s estimated compl. time on CPU is " + str(fJobs[keyId].estComplTimeCpu))
                    
        else:
            if (fJobs.get(keyId) is not None) and fJobs[keyId].estComplTimeGpu < 0:
                if (sJobs1.get(keyId) is not None) and (sJobs2.get(keyId) is not None):
                    if (sJobs1.get(keyId).complTime >= 0) and (sJobs2.get(keyId).complTime >= 0):
                        # linear model a * (numberofbatches) + b
                        a = (sJobs1[keyId].complTime - sJobs2[keyId].complTime) / (sJobs1[keyId].numBatches - sJobs2[keyId].numBatches)
                        b = sJobs1[keyId].complTime - a*sJobs1[keyId].numBatches
                        fJobs[keyId].estComplTimeGpu = a*fJobs[keyId].numBatches + b
                        print("[INFO] " + fJobs.get(keyId).jobName +"'s estimated compl. time on GPU is " + str(fJobs[keyId].estComplTimeGpu))  

        if  fJobs[keyId].estComplTimeCpu >= 0 and fJobs[keyId].estComplTimeGpu >= 0 and (not fJobs[keyId].isEstimated) : 
            if fJobs[keyId].estComplTimeGpu == 0:
                fJobs[keyId].estComplTimeGpu = 0.0001
            fJobs[keyId].estSpeedup = fJobs[keyId].estComplTimeCpu / fJobs[keyId].estComplTimeGpu
            print("[INFO] " + fJobs[keyId].jobName + "'s estimated speedup is "+ str(fJobs[keyId].estSpeedup))
            fJobs[keyId].isEstimated = True

def estimateSpeedup(fJobs, cJobs, gJobs):
    for keyId in fJobs:    
        if (fJobs.get(keyId) is not None) and (not fJobs[keyId].isEstimated):
            if (cJobs.get(keyId) is not None) and (gJobs.get(keyId) is not None):
                if (cJobs.get(keyId).complTime >= 0) and (gJobs.get(keyId).complTime >= 0):
                    # linear model a * (numberofbatches) + b
                    if gJobs[keyId].complTime == 0:
                        gJobs[keyId].complTime = 0.00001
                    fJobs[keyId].estSpeedup = cJobs[keyId].complTime / gJobs[keyId].complTime
                    print("[INFO] " + fJobs[keyId].jobName + "'s estimated speedup is "+ str(fJobs[keyId].estSpeedup))
                    fJobs[keyId].isEstimated = True
                            

def submitJob(podName, job_folder, yamfile, username):
    print("[INFO] Submit job " + podName)
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

def createSubCommands(cmd, numbatches):
    tempArray = cmd.split("--num_batches=")
    if len(tempArray) == 2:            
        subCmd1 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch1Percent))
        subCmd2 = tempArray[0] + " --num_batches=" + str(int(numbatches*numBatch2Percent))
    else:
        print("[ERROR] command shoud have --num_batches= at the end")

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

def submitJobs(fJobs):
    # deletedKeys = []
    for jobKey in fJobs:
        if fJobs[jobKey].isEstimated:
        # if fJobs[jobKey].estComplTimeCpu >=0 and fJobs[jobKey].estComplTimeGpu >=0::
            jobInfo = fJobs[jobKey]
            if not jobInfo.isSubmitted:                
                job = jobInfo.job            
                cpuCmd = job.cpuProfile.jobCmd
                gpuCmd = job.gpuProfile.jobCmd

                cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
                gpu_usage = Resource(1*MILLI, gpuMem *GI, gpu)
                activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobKey, cpuCmd, gpuCmd)
                prefix = jobInfo.userName
                yamfile = jobInfo.jobName
                createYamlFile(activeJob, prefix, yamfile, False, (not IS_MEASURE))            

                submitJob(jobInfo.jobName, job_folder, yamfile, jobInfo.userName) 
                jobInfo.isSubmitted=True
            # deletedKeys.append(jobKey)

        if IS_MEASURE:
            if fJobs[jobKey].isEstimated:
        # if fJobs[jobKey].estComplTimeCpu >=0 and fJobs[jobKey].estComplTimeGpu >=0::
                jobInfo = fJobs[jobKey]
                if not jobInfo.isSubmittedGpu:
                    job = jobInfo.job
                    cpuCmd = job.cpuProfile.jobCmd
                    gpuCmd = job.gpuProfile.jobCmd

                    cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
                    gpu_usage = Resource(1*MILLI, gpuMem *GI, gpu)
                    activeJob = ActiveJob(gpu_usage,cpu_usage,  0, 0, jobKey, gpuCmd, cpuCmd)
                    prefix = GPU_PREFIX + jobInfo.userName
                    yamfile = GPU_PREFIX + jobInfo.jobName
                    createYamlFile(activeJob, prefix, yamfile, True, False)            
                    submitJob(yamfile, job_folder, yamfile, jobInfo.userName) 
                    jobInfo.isSubmittedGpu=True

numBatch1Percent = 5.0/100
numBatch2Percent = 10.0/100
# numBatch2 = 200
FOLDER = "automation_tool"
GI = 1024*1024*1024
SCHEDULER = "kube-scheduler"
MY_SCHEDULER = "my-scheduler"
DEFAULT_NS = "default"
cpu=21
mem=16

gpuCpu=1
gpu=1
gpuMem=32

if IS_TEST:
    userStrArray = ["user1"]
else:
    userStrArray = ["user1", "user2", "user3", "user4"]   

this_path = os.path.dirname(os.path.realpath(__file__))
job_folder = this_path + "/" + FOLDER 
shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
os.mkdir(job_folder)    
workload = "traces/automation"
################################### MAIN Script ###############################################

print "====== AUTOMATION-TOOL ====="

def main():
    ## initialization   
    print "====== main() ====="
    users = []
    fullJobs = {}
    cpuShortJobs_1 = {}
    cpuShortJobs_2 = {}
    gpuShortJobs_1 = {}
    gpuShortJobs_2 = {}

    # read jobs from files to jobs
    for i in range(len(userStrArray)):
        strUser=userStrArray[i]
        # print("read " + strUser)
        jobs    = readJobs(this_path+"/"+workload, strUser+".txt", 1)
        newUser = User(strUser, jobs)
        # print(newUser.toString())
        users.append(newUser)
        # create user name space
        f = open(job_folder + '/' + newUser.username + ".yaml",'w')
        f.write(strUserYaml(newUser.username))
        f.close()
        print("kubectl create -f  " + job_folder + '/' + newUser.username+ ".yaml" )
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
            fullJobs[jobIdKey]  = JobInfo(jobId, jobName, user.username, job.numBatches)
            fullJobs[jobIdKey].job = job
            # deleteJob(jobName, user.username)
            
            # read the number of batch from the job
            cpuCmd = job.cpuProfile.jobCmd
            gpuCmd = job.gpuProfile.jobCmd
            cpuCmd1, cpuCmd2 = createSubCommands(cpuCmd, job.numBatches)        
            gpuCmd1, gpuCmd2 = createSubCommands(gpuCmd, job.numBatches)

            # for the small number of batches
            cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
            gpu_usage = Resource(1*MILLI, gpuMem *GI, gpu)

            # prepare jobs for CPU        
            prefix = "cpu1"
            jobName = prefix + "-" + str(jobId)
            yamfile = jobName
            numBatch1 = job.numBatches * numBatch1Percent
            newJob = JobInfo(jobId, jobName, user.username, numBatch1)
            activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId, cpuCmd1, gpuCmd1)
            createYamlFile(activeJob, prefix, yamfile, False, False)
            submitJob(jobName, job_folder, yamfile, DEFAULT_NS)        
            cpuShortJobs_1[jobIdKey] = newJob

            # prefix = "cpu2"
            # jobName = prefix + "-" + str(jobId)
            # yamfile = jobName
            # newJob  = JobInfo(jobId, jobName, user.username, numBatch2)
            # activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId,  cpuCmd2, gpuCmd2)
            # createYamlFile(activeJob, prefix, yamfile, False, False)
            # submitJob(jobName, job_folder, yamfile, DEFAULT_NS)        
            # cpuShortJobs_2[jobIdKey] = newJob

            # prepare jobs for GPU        
            prefix = "gpu1"
            jobName = prefix + "-" + str(jobId)
            yamfile = jobName
            newJob = JobInfo(jobId, jobName, user.username, numBatch1)
            activeJob = ActiveJob(gpu_usage, cpu_usage,  0, 0, jobId, gpuCmd1, cpuCmd1 )
            createYamlFile(activeJob, prefix, yamfile, True, False)
            submitJob(jobName, job_folder, yamfile, DEFAULT_NS)        
            gpuShortJobs_1[jobIdKey] = newJob

            # prefix = "gpu2"
            # jobName = prefix + "-" + str(jobId)
            # yamfile = jobName
            # newJob  = JobInfo(jobId, jobName, user.username, numBatch2)
            # activeJob = ActiveJob(gpu_usage, cpu_usage,  0, 0, jobId, gpuCmd2,  cpuCmd2)
            # createYamlFile(activeJob, prefix, yamfile, True, False)
            # submitJob(jobName, job_folder, yamfile, DEFAULT_NS)        
            # gpuShortJobs_2[jobIdKey] = newJob
 
            
            startedJobs, completedJobs, currTime = listJobStatus()
            updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
            updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
            
            estimateSpeedup(fullJobs, cpuShortJobs_1, gpuShortJobs_1)
            # estimateSpeedup(fullJobs, gpuShortJobs_1, gpuShortJobs_2, False)

            # submitJobs(fullJobs)

            if IS_MEASURE:
                updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, False)
                updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, True)

    submitJobs(fullJobs)        
    # step 4: measure the job completion time.
    started = False
    rows = []
  
    iTime = 0
    infiniteLoop = True
    if IS_TEST:
        infiniteLoop = False
    while infiniteLoop:
        sleep(interval)
        startedJobs, completedJobs, currTime = listJobStatus()
        updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1,currTime)
        # updateJobInfo(startedJobs, completedJobs, cpuShortJobs_2,currTime)
        updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1,currTime)
        # updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2,currTime)
        
        # step 5: estimation
        estimateSpeedup(fullJobs, cpuShortJobs_1, gpuShortJobs_1)
        
        # print("startedJobs: " + str(startedJobs))
        # print("completedJobs: " + str(completedJobs))
        # print("fullJobs: " + fullJobs["1"].jobName)
        if IS_MEASURE:
            updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, False)
            updateFullJobInfo(startedJobs, completedJobs, fullJobs, currTime, True)
        # step 6: submit profiled jobs to the system
        # print ("size of full jobs: " + str(len(fullJobs)))
        submitJobs(fullJobs)   
             

        if (iTime % 60 == 0): # write down every 1 min.
            # step 6: write results out
            writeJobsToCsv(fullJobs,'est_results')
            writeJobsToCsv(cpuShortJobs_1,'cpuShortJobs_1')    
            writeJobsToCsv(gpuShortJobs_1,'gpuShortJobs_1') 
        iTime = iTime + interval      

if __name__ == "__main__": main()