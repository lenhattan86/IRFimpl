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
SCHEDULER = "my-scheduler"
jobId = 0
inputData="""user1
python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0  --model=alexnet --batch_size=32 --num_intra_threads=19 --num_batches=10
python tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0  --model=alexnet --batch_size=32 --num_batches=10
16.0 0 12 30
1.0 2 1 10
user2
python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0  --model=alexnet --batch_size=32 --num_intra_threads=19 --num_batches=10
python tf_cnn_benchmarks.py --device=gpu --num_warmup_batches=0  --model=alexnet --batch_size=32 --num_batches=10
16.0 0 12 30
1.0 2 1 10
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

        pri_usage = Resource(priCpu*MILLI, priMem *GI, priGpu)
        sec_usage = Resource(secCpu*MILLI, secMem *GI, secGpu)

        activeJob = ActiveJob(pri_usage, sec_usage, 0, 0, jobId, priCmd, secCmd, primComplt, secComplt)
        f_yaml = open(job_folder + '/' + user+ "-"+str(jobId)+ ".yaml",'w')   
        f_yaml.write(strPodYaml(user, activeJob, SCHEDULER , priGpu>0))
        jobId= jobId + 1

    lineNum = lineNum + 1