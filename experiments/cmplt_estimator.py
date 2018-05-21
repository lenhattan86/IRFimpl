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

print "====== ONLINE-PERFORMANCE-ESTIMATION-TOOL ====="

STOP_TIME = -1
FOLDER = "cmplt_estimator"
GI = 1024*1024*1024
SCHEDULER = "my-scheduler"
this_path = os.path.dirname(os.path.realpath(__file__))


IS_TEST=True

if not IS_TEST:
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', help='cpu or gpu', required=True)
    parser.add_argument('--cmd', help='full command', required=True)
    args = vars(parser.parse_args())
    
    device = args['device']
    cmd = args['cmd']    
else:
    device='cpu'
    cmd=''

def readJobStatus(podName):
    isFinished = False
    isStarted = False
    rows=[]
    now = datetime.datetime.now()        
    # p = subprocess.Popen(["kubectl get pods --all-namespaces --field-selector=status.phase!=Pending"], 
    p = subprocess.Popen(["kubectl get pods --all-namespaces"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    if IS_TEST:
            output = """NAMESPACE     NAME                                       READY     STATUS      RESTARTS   AGE
default       job-alexnet-cpu-0                          0/1       Completed   0          19h
default       job-alexnet-cpu-1                          0/1       Completed   0          19h
"""
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
            if mPodName == podName:
                if podStatus == "Pending":
                    continue
                if podStatus == "Completed":
                    isFinished = True
                if podStatus == "ContainerCreating" or podStatus == "Running":
                    isStarted = True                                 

    return isStarted, isFinished, podStatus

# step 1: read the job info
numBatches  = 200
jobName     = 'alexnet'
batchSize   = 32
common = "--model="+jobName+" --batch_size="+str(batchSize)+" --num_intra_threads=19 --num_batches="
CPU_COMMAND = "python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0" + common + str(numBatches)
GPU_COMMAND = "python tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0 " + common + str(numBatches)
# step 2: read the configure of servers
# cpus   per a node
# gpus   per a node
# memory per a node
if device.lower() == "cpu":
    cpu=16
    gpu=0
    mem=32
elif device.lower() == "gpu":
    cpu=1
    gpu=1
    mem=32
else:
    print("[ERROR] Invalid device: " + cpu)
    sys.exit()

# step 3: submit job to Kubernetes

job_folder = this_path + "/" + FOLDER 
shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
os.mkdir(job_folder)    

smallNumBatches = 10
cpu_usage = Resource(cpu*MILLI, mem, 0)
gpu_usage = Resource(cpu     , mem, 1)
cpuFullCommand = "python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0 " + common + str(smallNumBatches)
gpuFullCommand = "python tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0  " + common + str(smallNumBatches)

    # prepare jobs
yamfile = jobName
jobId    = 1
activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId, cpuFullCommand, gpuFullCommand)
f_yaml = open(job_folder + '/' + yamfile+ ".yaml",'w')   
f_yaml.write(strPodYaml('job', activeJob, SCHEDULER, False))
f_yaml.close()
    # submit jobs

print("Submit job " + cpuFullCommand)
p = subprocess.Popen(["kubectl create -f " + job_folder + '/' + yamfile+ ".yaml"], 
        stdout=subprocess.PIPE, shell=True)                   
(output, err) = p.communicate()    
p_status = p.wait() 

# step 4: measure the job completion time.
print("Start monitoring the job "+jobName)
start = time()
# podName = "job-"+str(jobId)
podName = "job-alexnet-cpu-0"
started = False
rows = []
while True: 
    isStarted, isFinished, podStatus = readJobStatus(podName)   
    if isStarted and (not started): 
        start = time()
        print("job  started ... ")
        started = True
    if isFinished:
        end = time()
        complTime = end - start
        print("job  completed ... ")
        row = [podName, start , end, podStatus] 
        rows.append(row) 
        break
    sleep(1)

print(complTime)

# step 5: write results out
print(job_folder)
ofile  = open(job_folder + '/' + 'online_tool.csv', "wb")
writer = csv.writer(ofile, dialect='excel')
writer.writerows(rows) 