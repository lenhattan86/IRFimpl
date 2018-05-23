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

if IS_TEST:
    print("please indicate --test=False")

interval=1
def listJobStatus():
    startedPods   = []
    completedPods = []
    # p = subprocess.Popen(["kubectl get pods --all-namespaces --field-selector=status.phase!=Pending"], 
    p = subprocess.Popen(["kubectl get pods --all-namespaces"], 
    # p = subprocess.Popen(["kubectl get pods " + podName], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    if IS_TEST:
        output = """NAMESPACE     NAME                                       READY     STATUS      RESTARTS   AGE
user1       cpu1-1                          0/1       ContainerCreating   0          19h
user1       cpu1-1                          0/1       Completed   0          19h
user1       cpu2-1                          0/1       ContainerCreating   0          19h
user1       cpu2-1                          0/1       Completed   0          19h
user1       user1-1                          0/1       ContainerCreating   0          19h
user1       user1-1                          0/1       Completed   0          19h
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

def estimate(fJobs, sJobs1, sJobs2, isCPU):
    for keyId in fJobs:    
        if isCPU:
            if (fJobs.get(keyId) is not None) and fJobs[keyId].estComplTimeCpu < 0:
                if (sJobs1.get(keyId) is not None) and (sJobs2.get(keyId) is not None):
                    if (sJobs1.get(keyId).complTime >= 0) and (sJobs2.get(keyId).complTime >= 0):
                        # linear model a * (numberofbatches) + b
                        a = (sJobs1[keyId].complTime - sJobs2[keyId].complTime) / (sJobs1[keyId].numBatches - sJobs2[keyId].numBatches)
                        b = sJobs1[keyId].complTime - a*sJobs1[keyId].numBatches                        
                        fJobs[keyId].estComplTimeCpu = a*fJobs[keyId].numBatches + b
                        print("[INFO] " + fJobs.get(keyId).jobName +"'s estiated compl. time on CPU is " + str(fJobs[keyId].estComplTimeCpu))
                    
        else:
            if (fJobs.get(keyId) is not None) and fJobs[keyId].estComplTimeGpu < 0:
                if (sJobs1.get(keyId) is not None) and (sJobs2.get(keyId) is not None):
                    if (sJobs1.get(keyId).complTime >= 0) and (sJobs2.get(keyId).complTime >= 0):
                        # linear model a * (numberofbatches) + b
                        a = (sJobs1[keyId].complTime - sJobs2[keyId].complTime) / (sJobs1[keyId].numBatches - sJobs2[keyId].numBatches)
                        b = sJobs1[keyId].complTime - a*sJobs1[keyId].numBatches
                        fJobs[keyId].estComplTimeGpu = a*fJobs[keyId].numBatches + b
                        print("[INFO] " + fJobs.get(keyId).jobName +"'s estiated compl. time on GPU is " + str(fJobs[keyId].estComplTimeGpu))        


def submitJob(podName, job_folder, yamfile, username):
    print("Submit job " + podName)
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

def createSubCommands(cmd):
    tempArray = cmd.split("--num_batches=")
    if len(tempArray) == 2:            
        subCmd1 = tempArray[0] + " --num_batches=" + str(numBatch1)
        subCmd2 = tempArray[0] + " --num_batches=" + str(numBatch2)
    else:
        print("[ERROR] command shoud have --num_batches= at the end")

    return subCmd1, subCmd2

def createYamlFile(activeJob, prefix, yamfile, isGPU):
    f_yaml = open(job_folder + '/' + yamfile+ ".yaml",'w')   
    f_yaml.write(strPodYaml(prefix, activeJob, SCHEDULER, isGPU))
    f_yaml.close()    

def submitJobs(fJobs):
    deletedKeys = []
    for jobKey in fJobs:
        if fJobs[jobKey].estComplTimeCpu >=0:
        # if fJobs[jobKey].estComplTimeCpu >=0 and fJobs[jobKey].estComplTimeGpu >=0::
            jobInfo = fJobs[jobKey]
            job = jobInfo.job            
            cpuCmd = job.cpuProfile.jobCmd
            gpuCmd = job.gpuProfile.jobCmd

            cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
            gpu_usage = Resource(cpu*MILLI, gpuMem *GI, gpu)
            activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobKey, cpuCmd, gpuCmd)
            prefix = jobInfo.userName
            yamfile = jobInfo.jobName
            createYamlFile(activeJob, prefix, yamfile, False)            

            submitJob(jobInfo.jobName, job_folder, yamfile, jobInfo.userName)            
            deletedKeys.append(jobKey)
    
    for jobKey in deletedKeys:
        del fJobs[jobKey]



################################### MAIN Script ###############################################

## initialization
print "====== ONLINE-PERFORMANCE-ESTIMATION-TOOL ====="

STOP_TIME = -1
FOLDER = "automation_tool"
GI = 1024*1024*1024
SCHEDULER = "kube-scheduler"
this_path = os.path.dirname(os.path.realpath(__file__))

job_folder = this_path + "/" + FOLDER 
shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
os.mkdir(job_folder)    

cpu=16
mem=16

gpuCpu=1
gpu=1
gpuMem=32
workload = "traces/automation"
userStrArray = ["user1"]

users = []
fullJobs = {}
numBatch1 = 0
numBatch2 = 20
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
    p = subprocess.Popen(["kubectl create -f  " + job_folder + '/' + newUser.username+ ".yaml" ],
            stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait()

# create profiling jobs
jobId = 0
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
        cpuCmd1, cpuCmd2 = createSubCommands(cpuCmd)        
        gpuCmd1, gpuCmd2 = createSubCommands(cpuCmd)

        # for the small number of batches
        cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
        gpu_usage = Resource(cpu*MILLI, gpuMem *GI, gpu)

        # prepare jobs for CPU        
        prefix = "cpu1"
        jobName = prefix + "-" + str(jobId)
        yamfile = jobName
        newJob = JobInfo(jobId, jobName, user.username, numBatch1)
        activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId, cpuCmd1, gpuCmd1)
        createYamlFile(activeJob, prefix, yamfile, False)
        submitJob(jobName, job_folder, yamfile, user.username)        
        cpuShortJobs_1[jobIdKey] = newJob

        prefix = "cpu2"
        jobName = prefix + "-" + str(jobId)
        yamfile = jobName
        newJob  = JobInfo(jobId, jobName, user.username, numBatch2)
        activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId,  cpuCmd2, gpuCmd2)
        createYamlFile(activeJob, prefix, yamfile, False)
        submitJob(jobName, job_folder, yamfile, user.username)        
        cpuShortJobs_2[jobIdKey] = newJob

        # prepare jobs for GPU
        # jobId     = jobId + 1
        # jobName = "job" + str(jobId)
        # yamfile = jobName
        # newJob = JobInfo(jobName, user.username)
        # activeJob = ActiveJob(gpu_usage, cpu_usage, 0, 0, jobId,  gpuFullCommand, cpuFullCommand)
        # createYamlFile(activeJob)
        # submitJob(jobName, job_folder, yamfile)
        # gpuShortJobs_1.append(newJob)
        
        startedJobs, completedJobs, currTime = listJobStatus()
        updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1, currTime)
        updateJobInfo(startedJobs, completedJobs, cpuShortJobs_2, currTime)
        updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1, currTime)
        updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2, currTime)
        
        estimate(fullJobs, cpuShortJobs_1, cpuShortJobs_2, True)
        estimate(fullJobs, gpuShortJobs_1, gpuShortJobs_2, False)

        # updateJobInfo(startedJobs, completedJobs, fullJobs, currTime)

# step 4: measure the job completion time.
started = False
rows = []
endTime = 2
iTime = 0
infiniteLoop = True
if IS_TEST:
    infiniteLoop = False
while iTime < endTime or infiniteLoop:
    sleep(interval)
    startedJobs, completedJobs, currTime = listJobStatus()
    updateJobInfo(startedJobs, completedJobs, cpuShortJobs_1,currTime)
    updateJobInfo(startedJobs, completedJobs, cpuShortJobs_2,currTime)
    updateJobInfo(startedJobs, completedJobs, gpuShortJobs_1,currTime)
    updateJobInfo(startedJobs, completedJobs, gpuShortJobs_2,currTime)
    
    # step 5: estimation
    estimate(fullJobs, cpuShortJobs_1, cpuShortJobs_2, True)
    estimate(fullJobs, gpuShortJobs_1, gpuShortJobs_2, False)
    
    updateJobInfo(startedJobs, completedJobs, fullJobs, currTime)
    # step 6: submit profiled jobs to the system
    # print ("size of full jobs: " + str(len(fullJobs)))
    submitJobs(fullJobs)   
    iTime = iTime + 1       

# step 6: write results out
ofile  = open(job_folder + '/' + 'cmplt_estimator.csv', "wb")
writer = csv.writer(ofile, dialect='excel')
writer.writerows(rows) 