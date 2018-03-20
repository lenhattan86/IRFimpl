#!/usr/bin/env python

# Copyright 2016 Tan N. Le
# lenhattan86@gmail.com

import argparse
import time
import json
import sys
import urllib2
import csv
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--user', help='YARN ResourceManager URL', required=True)
parser.add_argument('--interval', help='Polling interval', required=True)
parser.add_argument('--file', help='log file', required=True)

args = vars(parser.parse_args())

interval = int(args['interval'])
user = args['user']
file_name = args['file']

ofile  = open(file_name, "wb")
writer = csv.writer(ofile, dialect='excel')

while True:
    p = subprocess.Popen(["kubectl get pods ", "--show-all ", "--namespace=" + user], 
        stdout=subprocess.PIPE, shell=True)         
    (output, err) = p.communicate()
    p_status = p.wait()
    # print "Command output : ", output    
    if p_status != 0:        
        print 'Could not access the kubernetes'
        break
    else:
        # TODO: 
        #row = [timestamp, user, podName]
        row = "[timestamp, user, podName]"
        writer.writerow(row)

    time.sleep(interval)
    




