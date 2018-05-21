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
            podName=strArr[1]
            podStatus=strArr[3]
            if podStatus == "Pending":
                continue
            if podStatus == "Completed":
                isFinished = True
            if podStatus == ""
                isStarted = True                

    return isStarted, isFinished

# step 1: read the job info

# step 2: read the configure of servers
    # cpus   per a node
    # gpus   per a node
    # memory per a node
# 

# step 3: submit job to Kubernetes

# step 4: measure the job completion time.
start = time.time()
podName = 'job-alexnet-cpu-0'
while True:    
    sleep(1)
    isStarted, isFinished = readJobStatus(podName)   
    if isFinished :
        end = time.time()
        complTime = end - start        
        break
        
print(complTime)