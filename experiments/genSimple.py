import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *

#  gen simple yaml file

job_folder = "experiments/testcases/simple_google"
user = "user1"
a = 2
# user = "user2"
# a = 6

jobId = 0
inputData="""# 0
1 0 1 0 queue0
stage -1.0 4.0 6 3 1 2 1 1
0
# 1
1 1 1 0 queue1
stage -1.0 4.0 7 16 1 2 7 1
0
# 2
1 2 1 0 queue0
stage -1.0 4.0 3 18 1 2 14 1
0
# 3
1 3 1 0 queue1
stage -1.0 4.0 10 16 1 2 3 1
0
# 4
1 4 1 0 queue0
stage -1.0 4.0 10 16 1 2 17 1
0
# 5
1 5 1 0 queue1
stage -1.0 4.0 10 6 1 2 1 1
0
# 6
1 6 1 0 queue0
stage -1.0 5.0 2 2 1 2 13 1
0
# 7
1 7 1 0 queue1
stage -1.0 4.0 10 6 1 2 4 1
0
# 8
1 8 1 0 queue0
stage -1.0 4.0 10 6 1 2 2 1
0
# 9
1 9 1 0 queue1
stage -1.0 15.0 16 2 1 2 3 1
0
# 10
1 10 1 0 queue0
stage -1.0 15.0 11 2 1 2 4 1
0
# 11
1 11 1 0 queue1
stage -1.0 4.0 16 19 1 2 2 1
0
# 12
1 12 1 0 queue0
stage -1.0 4.0 16 16 1 2 3 1
0
# 13
1 13 1 0 queue1
stage -1.0 4.0 16 19 1 2 7 1
0
# 14
1 14 1 0 queue0
stage -1.0 15.0 16 15 1 2 11 1
0
# 15
1 15 1 0 queue1
stage -1.0 15.0 16 18 1 2 7 1
0
# 16
1 16 1 0 queue0
stage -1.0 15.0 16 12 1 2 5 1
0
# 17
1 17 1 0 queue1
stage -1.0 4.0 16 16 1 2 4 1
0
# 18
1 18 1 0 queue0
stage -1.0 4.0 16 20 1 2 5 1
0
# 19
1 19 1 0 queue1
stage -1.0 15.0 7 1 1 2 1 1
0
"""
lineNum = 0
lines = inputData.split('\n')
for line in lines:
    if lineNum % 8 == a:
        print line
        strs=line.split(" ")
        cpu = float(strs[2])
        mem = int(strs[3])
        cpuComplt = int(strs[4]) * 10
        gpuComplt = int(strs[7]) * 10
        gpuMem = 2

        cpu_usage = Resource(cpu*MILLI, mem *GI, 0)
        gpu_usage = Resource(1*MILLI, gpuMem *GI, 1)

        SCHEDULER = "my-scheduler"
        cmd = "sleep " + str(cpuComplt)
        seJobCmd = "sleep " + str(gpuComplt)
        activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, jobId,cmd, seJobCmd, cpuComplt, gpuComplt)
        f_yaml = open(job_folder + '/' + user+ "-"+str(jobId)+ ".yaml",'w')   
        f_yaml.write(strPodYaml('user', activeJob,SCHEDULER , False))
        jobId= jobId + 1

    lineNum = lineNum + 1