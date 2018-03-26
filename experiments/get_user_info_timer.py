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


# parser = argparse.ArgumentParser()
# parser.add_argument('--user', help='YARN ResourceManager URL', required=True)
# parser.add_argument('--interval', help='Polling interval  (secs)', required=True)
# parser.add_argument('--file', help='csv file', required=True)
# parser.add_argument('--stopTime', help='stop time (secs)', required=True)
# args = vars(parser.parse_args())

# interval = int(args['interval'])
# user = args['user']
# file_name = args['file']
# stop_time = int(args['stopTime'])

interval=1
user="user1"
file_name="user1.csv"
stop_time=-1

def capture(timeStep, writer):
    now = datetime.datetime.now()        
    p = subprocess.Popen(["kubectl get pods --show-all --namespace=" + user], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 

    output = """NAME                READY     STATUS      RESTARTS   AGE
job-alexnet-cpu-0   0/1       OOMKilled   0          52m
job-alexnet-gpu-0   0/1       Completed   0          52m
"""
    p_status=0    

    completedJobs = 0
    # time_step = time_step + interval
    if p_status != 0:        
        print 'Could not access the kubernetes'
    else:
        lines=output.split("\n")                
        for line in lines[1:len(lines)-1]:            
            strArr=line.split()            
            podName=strArr[0]
            podStatus=strArr[2]
            row = [now, timeStep, user, podName, podStatus]                            
            writer.writerow(row)
            if (podStatus == "Completed") or (podStatus == "OOMKilled") or(podStatus == "Error"):
                completedJobs = completedJobs + 1

# this_path = os.path.dirname(os.path.realpath(__file__))
# ofile  = open(this_path  + "/" + file_name, "wb")
ofile  = open(file_name, "wb")
writer = csv.writer(ofile, dialect='excel')
mTime = 1
# for mTime in range(int(stop_time/interval)):
while True:        
    if (stop_time > 0 and mTime*interval > stop_time):        
        break
    Timer(mTime*interval, capture, [mTime, writer]).start()        
    mTime = mTime + 1