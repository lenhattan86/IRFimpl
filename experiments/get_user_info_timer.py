#!/usr/bin/env python

# Copyright 2016 Tan N. Le
# lenhattan86@gmail.com

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


parser = argparse.ArgumentParser()
parser.add_argument('--interval', help='Polling interval  (secs)', required=True)
parser.add_argument('--file', help='csv file', required=True)
parser.add_argument('--stopTime', help='stop time (secs)', required=True)
args = vars(parser.parse_args())

interval = int(args['interval'])
file_name = args['file']
stop_time = int(args['stopTime'])

# interval=1
# file_name="user1.csv"
# stop_time=1

def capture(timeStep, writer):
    now = datetime.datetime.now()        
    p = subprocess.Popen(["kubectl get pods --all-namespaces --field-selector=status.phase!=Pending"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 

#     output = """NAMESPACE     NAME                                       READY     STATUS      RESTARTS   AGE
# default       job-alexnet-cpu-0                          0/1       Completed   0          19h
# default       job-alexnet-cpu-1                          0/1       Completed   0          19h
# """
#     p_status=0    

    completedJobs = 0
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
            row = [now, timeStep, user, podName, podStatus]                            
            writer.writerow(row)
            if (podStatus == "Completed") or (podStatus == "OOMKilled") or(podStatus == "Error"):
                completedJobs = completedJobs + 1


def captureResource(timeStep, writer):
    now = datetime.datetime.now()        
    p = subprocess.Popen(["kubectl get node --no-headers -o custom-columns=NAME:.metadata.name"], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 

#     output = """k80-1
# k80-2
# """
#     p_status=0    

    if p_status != 0:        
        print 'Could not access the kubernetes'
    else:
        lines=output.split("\n")                
        for line in lines[1:len(lines)-1]:            
            node=line
            nodeCmd = "kubectl describe node "+ node +" | sed '1,/kube-system/d'"
            p = subprocess.Popen([nodeCmd], 
                stdout=subprocess.PIPE, shell=True)                   
            (mOutput, err) = p.communicate()    
            p_status = p.wait() 
#             p_status=0
#             mOutput="""kube-system                calico-node-f8trv                            250m (0%)     0 (0%)      0 (0%)           0 (0%)
#   kube-system                calico-policy-controller-5cf6666d98-958q6    0 (0%)        0 (0%)      0 (0%)           0 (0%)
#   kube-system                etcd-k80-1                                   0 (0%)        0 (0%)      0 (0%)           0 (0%)
#   kube-system                kube-apiserver-k80-1                         250m (0%)     0 (0%)      0 (0%)           0 (0%)
#   kube-system                kube-controller-manager-k80-1                200m (0%)     0 (0%)      0 (0%)           0 (0%)
#   kube-system                kube-proxy-kvhfk                             0 (0%)        0 (0%)      0 (0%)           0 (0%)
#   kube-system                kube-scheduler-k80-1                         100m (0%)     0 (0%)      0 (0%)           0 (0%)
#   kube-system                my-scheduler-7b5fcd755f-b8wf9                100m (0%)     0 (0%)      0 (0%)           0 (0%)
#   user2                      user2-373                                    16 (33%)      16 (33%)    12Gi (9%)        12Gi (9%)
# Allocated resources:
#   (Total limits may be over 100 percent, i.e., overcommitted.)
#   CPU Requests  CPU Limits  Memory Requests  Memory Limits
#   ------------  ----------  ---------------  -------------
#   16900m (35%)  16 (33%)    12Gi (9%)        12Gi (9%)
# Events:         <none>
# """
            mLines= mOutput.split("\n")
            for mLine in mLines[0:len(mLines)-1]:
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
                writer.writerow(row)


if os.path.exists(file_name): 
    os.remove(file_name)
resFile = 'allocatedRes.csv'
if os.path.exists(resFile): 
    os.remove(resFile)

ofile  = open(file_name, "wb")
writer = csv.writer(ofile, dialect='excel')
oResfile  = open(resFile, "wb")
resWriter = csv.writer(oResfile, dialect='excel')

mTime = 1
# for mTime in range(int(stop_time/interval)):
while True:        
    if (stop_time > 0 and mTime*interval > stop_time):        
        break
    Timer(mTime*interval, capture, [mTime, writer]).start()        
    Timer(mTime*interval, captureResource, [mTime, resWriter]).start()
    mTime = mTime + 1