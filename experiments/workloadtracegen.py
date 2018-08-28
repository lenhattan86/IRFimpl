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

import shutil

class UserDemand:
    def __init__ (self):
        self.timestamps = []
        self.demands = []

class UserJob:
    def __init__ (self):
        self.benchmarks = []
        self.models = []
        self.minNumBatchs = []
        self.maxNumBatchs = []
        self.minBatchSizes = []
        self.maxBatchSizes = []
        self.minNumThreads = []
        self.maxNumThreads = []

def readDemand(demandfile):
    print('readDemand() has not been implemted yet.')
    userDemand = UserDemand()
    with open(demandfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            userDemand.timestamps.append(row[0])
            userDemand.demands.append(row[1])
            line_count = line_count + 1
        print('Processed '+ str(line_count) +' lines.')    

    return userDemand

def readJobs(job_file):
    userJob = UserJob()
    print('readJobs() has not been implemted yet.')

    with open(job_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            userJob.benchmarks.append(row[0].strip())
            userJob.models.append(row[1].strip())

            userJob.minNumBatchs.append(row[2].strip())
            userJob.maxNumBatchs.append(row[3].strip())

            userJob.minBatchSizes.append(row[4].strip())            
            userJob.maxBatchSizes.append(row[5].strip())

            userJob.minNumThreads.append(row[6].strip())
            userJob.maxNumThreads.append(row[7].strip())
            
            line_count = line_count + 1
        print('Processed '+ str(line_count) +' lines.')    
    
    return userJob

def genTFBenchmarkJob(model, cCpu, cMem, gCpu, gMem, num_threads, num_batches, batch_size, arrivalTime, jobName):
    strRes = str(arrivalTime) + " " + str(jobName) +"\n"
    strRes = strRes + str(cCpu) + " 0 " + str(cMem) + "\n"
    strRes = strRes + str(gCpu) + " "+str(1)+" "+str(gMem)+" 0" + "\n"
    strRes = strRes + "python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0  --model="+str(model)+" --batch_size="+str(batch_size)+" --num_intra_threads="+str(num_threads)+" --num_batches="+str(num_batches) + "\n"
    strRes = strRes + "python tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0  --model="+str(model)+" --batch_size="+str(batch_size)+" --num_batches="+str(num_batches) + "\n"
    return strRes

def genKerasJob(cCpu, cMem, gCpu, gMem, num_threads, num_batches, batch_size):
    strRes = "Not implemented yet"
    return strRes

def genUserTrace(user_file, user_demand, user_jobs, user):    
    ## Create the data to write into the file
    strData = ""    
    
    iDemand = 0
    demaneNumJobs = 0
    for iJob in range(len(user_jobs.benchmarks)):

        jobName = user+str(iJob)

        arrivalTime = user_demand.timestamps[iDemand]
        demand = user_demand.demands[iDemand]
        while (demand <= 0):
            iDemand = iDemand + 1
            demand = user_demand.demands[iDemand]
        
        benchmark = user_jobs.benchmarks[iJob]
        model = user_jobs.models[iJob]

        minNumBatch  = user_jobs.minNumBatchs[iJob]
        maxNumBatch  = user_jobs.maxNumBatchs[iJob]

        minBatchSize = user_jobs.minBatchSizes[iJob]
        maxBatchSize = user_jobs.maxBatchSizes[iJob]

        minNumThread = user_jobs.maxBatchSizes[iJob]
        maxNumThread = user_jobs.maxBatchSizes[iJob]        

        if benchmark == "tfbenchmark":
            strJob = genTFBenchmarkJob(model, maxCCpu, maxCMem, maxGCPU, maxGmem, maxNumThread, maxNumBatch, maxBatchSize, arrivalTime, jobName)
        # elif benchmark == "keras":
        #     print(user_jobs.models[iJob])
        else:
            print("[error] Unrecognize the benchmark " + str(benchmark))
        strData = strData + strJob

        demaneNumJobs = demaneNumJobs + 1
        if demaneNumJobs >= demand:
            demaneNumJobs = 0
    ## 
    f_user = open(user_file, 'w')       
    f_user.write(strData)
    f_user.close()

###################################### parameters #############################################

maxCCpu = 16000
maxCGpu = 0
maxCMem = 12

maxGCPU = 2000
maxGGpu = 1
maxGmem = 2

GEN_FOLDER = "tracegen_simple"
this_path  = os.path.dirname(os.path.realpath(__file__))
job_folder = this_path + "/" + GEN_FOLDER 
shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
os.mkdir(job_folder)    
userStrArray = ["user1"]
workload = "traces/workloadgen"
demandSuffix = "_demand.csv"
jobSuffix = "_jobs.txt"
workloadFolder = this_path + "/" + workload
################################### MAIN Script ###############################################

print "====== workload trace generation tool ====="

def main():
    ## initialization   
    print "====== main() ====="
    
    ## read demand
    userDemands = []
    userJobs    = []

    for user in userStrArray:
        # read user demand
        userDemandFile = workloadFolder + "/" + user + demandSuffix
        print("reading user demand file: " + userDemandFile)
        userdemand = readDemand(userDemandFile)
        userDemands.append(userdemand)

        # read the subset jobs for this user.
        userJobFile    = workloadFolder + "/" + user + jobSuffix
        print("reading user job file: " + userJobFile)
        userjob = readJobs(userJobFile)
        userJobs.append(userjob)

        # Create scripts for jobs.
        user_file = job_folder + "/" + user + ".txt"
        genUserTrace(user_file, userdemand, userjob, user)        

if __name__ == "__main__": main()