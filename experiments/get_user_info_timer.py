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


IS_TEST=False
if IS_TEST:
    print("=====get_user_info_timer TEST MODE====")
    sys.exit()

if not IS_TEST:
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', help='Polling interval  (secs)', required=False, default="1")
    parser.add_argument('--folder', help='folder to save csv files', required=False, default=".")
    parser.add_argument('--stopTime', help='stop time (secs)', required=False, default="1")
    args = vars(parser.parse_args())

    interval = float(args['interval'])
    folder = args['folder']
    stop_time = int(args['stopTime'])    
    writeStep=60/interval
    resCommandStep=1
    resWriteStep=writeStep*resCommandStep    
else:
    interval=1
    stop_time=4
    writeStep=2
    resCommandStep=2
    resWriteStep=writeStep*resCommandStep
    folder="."


podFile = folder+"/""pods.csv"
resFile = folder+"/"+'allocatedRes.csv'
podRows=[]
resRows=[]
podLock = threading.Lock()
resLock = threading.Lock()

def capture(timeStep, writer):
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
    if p_status != 0 or err != None:        
        print '[capture] Could not access the kubernetes'
        print err
    else:
        lines=output.split("\n")            
        for line in lines[1:len(lines)-1]:            
            strArr=line.split()            
            user=strArr[0]
            if user == "kube-system":
                continue
            podName=strArr[1]
            podStatus=strArr[3]
            # if podStatus == "Pending":
                # continue    
            row = [now, timeStep, user, podName, podStatus] 
            rows.append(row) 
            # if (podStatus == "Completed") or (podStatus == "OOMKilled") or(podStatus == "Error"):
            #     completedJobs = completedJobs + 1
    with podLock:    
        podRows.extend(rows)
        if len(podRows) > 0 and timeStep % writeStep == 0:            
            writer.writerows(podRows) 
            podRows[:]=[]

def captureResource(timeStep, writer):
    if timeStep % resCommandStep != 0:
        return
        
    rows = []
    now = datetime.datetime.now()        
    p = subprocess.Popen(["kubectl get node --no-headers -o custom-columns=NAME:.metadata.name"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    if IS_TEST:
        output = """k80-1
k80-2
"""
        p_status=0    

    if p_status != 0 or err != None:        
        print '[captureResource] Could not access the kubernetes'
        print err
    else:
        lines=output.split("\n")   
        # rows = []             
        for line in lines[0:len(lines)-1]:            
            node=line
            nodeCmd = "kubectl describe node "+ node +" | sed '1,/Non-terminated Pods/d'"
            p = subprocess.Popen([nodeCmd], 
                stdout=subprocess.PIPE, shell=True)                   
            (mOutput, err) = p.communicate()    
            p_status = p.wait() 
            if IS_TEST:
                p_status=0
                mOutput="""Namespace                  Name                                                           CPU Requests  CPU Limits  Memory Requests  Memory Limits
---------                  ----                                                           ------------  ----------  ---------------  -------------
  kube-system                calico-node-f8trv                            250m (0%)     0 (0%)      0 (0%)           0 (0%)
  kube-system                calico-policy-controller-5cf6666d98-958q6    0 (0%)        0 (0%)      0 (0%)           0 (0%)
  kube-system                etcd-k80-1                                   0 (0%)        0 (0%)      0 (0%)           0 (0%)
  kube-system                kube-apiserver-k80-1                         250m (0%)     0 (0%)      0 (0%)           0 (0%)
  kube-system                kube-controller-manager-k80-1                200m (0%)     0 (0%)      0 (0%)           0 (0%)
  kube-system                kube-proxy-kvhfk                             0 (0%)        0 (0%)      0 (0%)           0 (0%)
  kube-system                kube-scheduler-k80-1                         100m (0%)     0 (0%)      0 (0%)           0 (0%)
  kube-system                my-scheduler-7b5fcd755f-b8wf9                100m (0%)     0 (0%)      0 (0%)           0 (0%)
  user2                      user2-373                                    16 (33%)      16 (33%)    12Gi (9%)        12Gi (9%)
Allocated resources:if len(resRows) > 0 and timeStep % resWriteStep == 0:
        writer.writerows(resRows) 
        resRows[:]=[]
  (Total limits may be over 100 percent, i.e., overcommitted.)
  CPU Requests  CPU Limits  Memory Requests  Memory Limits
  ------------  ----------  ---------------  -------------
  16900m (35%)  16 (33%)    12Gi (9%)        12Gi (9%)
Events:         <none>
"""
            mLines= mOutput.split("\n")            
            for mLine in mLines[2:len(mLines)-1]:
                if mLine.startswith('Allocated resources:'):
                    break                                    
                strArr=mLine.split()            
                user=strArr[0]
                if user=="kube-system":
                    continue
                podName=strArr[1]
                cpuReq=strArr[2]
                cpuReqPercent = strArr[3]
                cpuLimit=strArr[4]
                cpuLimitPercent = strArr[5]
                memReq=strArr[6]
                memReqPercent = strArr[7]
                memLimit=strArr[8]
                memLimitPercent = strArr[9]
                
                row = [now, timeStep, user, podName, node, cpuReq, cpuLimit, memReq, memLimit]    
                rows.append(row) 
        # if len(rows) > 0:
        #     writer.writerows(rows)
    with resLock:
        resRows.extend(rows)
        if len(resRows) > 0 and timeStep % resWriteStep == 0:
            writer.writerows(resRows) 
            resRows[:]=[]

if os.path.exists(podFile): 
    os.remove(podFile)

if os.path.exists(resFile): 
    os.remove(resFile)

ofile  = open(podFile, "wb")
writer = csv.writer(ofile, dialect='excel')
oResfile  = open(resFile, "wb")
resWriter = csv.writer(oResfile, dialect='excel')

mTime = 1
# for mTime in range(int(stop_time/interval)):
# while True:        
#     if (stop_time > 0 and mTime*interval > stop_time):        
#         break
#     Timer(mTime*interval, capture, [mTime, writer]).start()        
#     if stop_time > 0:
#         Timer(mTime*interval, captureResource, [mTime, resWriter]).start()
#     mTime = mTime + 1
    
while True:        
    if (stop_time > 0 and mTime*interval > stop_time):        
        break
    capture(mTime, writer)
    captureResource(mTime, resWriter)    
    mTime = mTime + 1
    sleep(interval)