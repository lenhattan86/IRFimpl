import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *

#  gen simple yaml file

job_folder = "experiments/testcases/motivation"
a = 6
SCHEDULER = "my-scheduler"
jobId = 0
inputData="""user1
sleep 30
sleep 20
4.0 0 6 3
1 1 2 1 1
"""

lineNum = 0
lines = inputData.split('\n')
for line in lines:
    if lineNum % 5 == 0:
        user = line
    if lineNum % 5 == 1:
        priCmd = line 
    if lineNum % 5 == 2:
        secCmd = line
    if lineNum % 5 == 3:
        priDemand = line
    if lineNum % 5 == 4:
        secDemand = line
        strs=priDemand.split(" ")        
        priCpu = float(strs[0]) 
        priGpu = int(strs[1])      
        priMem = int(strs[2])
        primComplt = int(strs[3])

        strs=secDemand.split(" ")
        secCpu = float(strs[0])                
        secGpu = int(strs[1])
        secMem = int(strs[2])        
        secComplt = int(strs[3])

        cpu_usage = Resource(priCpu*MILLI, priMem *GI, priGpu)
        gpu_usage = Resource(secCpu*MILLI, secMem *GI, secGpu)

        activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId, priCmd, secCmd, primComplt, secComplt)
        f_yaml = open(job_folder + '/' + user+ "-"+str(jobId)+ ".yaml",'w')   
        f_yaml.write(strPodYaml(user, activeJob,SCHEDULER , priGpu>0))
        jobId= jobId + 1

    lineNum = lineNum + 1