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

parser = argparse.ArgumentParser()
parser.add_argument('--user', help='YARN ResourceManager URL', required=True)
parser.add_argument('--interval', help='Polling interval  (secs)', required=True)
parser.add_argument('--file', help='log file', required=True)
parser.add_argument('--stopTime', help='stop time (secs)', required=True)
args = vars(parser.parse_args())

interval = int(args['interval'])
user = args['user']
file_name = args['file']
stop_time = int(args['stopTime'])

# interval=1
# user="user1"
# file_name="user1.log"
# stop_time=10

# this_path = os.path.dirname(os.path.realpath(__file__))
# ofile  = open(this_path  + "/" + file_name, "wb")
ofile  = open(file_name, "wb")
writer = csv.writer(ofile, dialect='excel')

start_time=time()

while True:
    now = datetime.datetime.now()
    end_time = time()
    p = subprocess.Popen(["kubectl get pods --show-all --namespace=" + user], 
        stdout=subprocess.PIPE, shell=True)                   
    (output, err) = p.communicate()    
    p_status = p.wait() 
    #"""NAME                                       READY     STATUS    RESTARTS   AGE"""
    # p_status=0
    # writer.writerow([1, 2])
    elapse=end_time - start_time 
    if p_status != 0:        
        print 'Could not access the kubernetes'
        break
    else:
        lines=output.split("\n")
        for line in lines[2:len(lines)-1]:            
            strArr=line.split()            
            podName=strArr[0]
            podStatus=strArr[2]
            row = [now, elapse, user, podName, podStatus]
            writer.writerow(row)

    if (elapse > stop_time):
        print("stop after " + str(stop_time) + " seconds")
        break

    sleep(interval)