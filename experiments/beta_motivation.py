# this file generate the script to evaluate the impact of cpu on GPU jobs.
import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *


benchmarks = "tf_cnn_benchmarks.py"

# https://www.tensorflow.org/performance/benchmarks
NUM_JOBS = 3
GPU_CPU = 1
# GPU_CPU = 16

# JOB_NAMEs   = ['vgg11', 'vgg16', 'vgg19', 'lenet', 'googlenet', 'overfeat', 'alexnet', 'trivial', 'inception3', 'inception4', 'resnet50', 'resnet101', 'resnet152']
# BatchSizes  = [32,      32,      32,      32,      32,          32,         512,       32,        32,           64,           64,         64,          64, ]

# BatchSizes    = [512,    512,     512,     512,      512,        512,         512,       512,        512,           512,           512,         512,          512, ]
# BatchSizes    = [512,    512,     512,     512,      512,        512,         512,       512,        512,           512,           512,         512,          512, ]

JOB_NAMEs   = ['vgg16', 'lenet', 'googlenet', 'alexnet', 'trivial', 'resnet50', 'inception3']
BatchSizes  = [32     ,  32     ,         32,      512,         32,         64,           64]

CPU = 16
NUM_THREADs = 16
MEM = 3

BatchNUm = 200

CPU_COMMAND = "python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC "
GPU_COMMAND = "python tf_cnn_benchmarks.py --device=gpu "
 #--model=alexnet --batch_size=16 --num_batches=200 --num_gpus=1
MILLI=1000


##########################

STOP_TIME = 36000
FOLDER = "beta_motivation"
GI = 1024*1024*1024
SCHEDULER = "kube-scheduler"
this_path = os.path.dirname(os.path.realpath(__file__))

def shellProfiling(job_folder, job_number, gpuCmd, exp_name, stopTime):    
    shellFile = job_folder + "/profiling.sh"
    f = open(shellFile,'w')
    strShell = ""   

    strShell = strShell + "kubectl delete pods --all --namespace=default --grace-period=0 --force \n"
    strShell = strShell + "echo wait... \n"
    strShell = strShell + "sleep 60 \n"
    
    strShell = strShell + "sudo docker pull lenhattan86/gpu \n"
    
    strShell = strShell + "python ../get_user_info_timer.py " \
        " --interval="+str(1) + " --stopTime="+str(stopTime)+" --file="+exp_name+".csv & pythonScript=$! \n"  

    ## create GPU jobs
    shellJobs(job_folder, job_number, gpuCmd, exp_name)

    strShell = strShell + "./" +exp_name+".sh & cpuScript=$! \n"               

    strShell = strShell + "wait"    
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def shellJobs(job_folder, job_number, cmd, fileName):
    
    ## create yaml files
    strShell = ""
    strLogShell = ""
    miliCPU = CPU*MILLI
    mem = MEM*GI
    cpu_usage = Resource(miliCPU, mem, 0)
    gpu_usage = Resource(GPU_CPU*MILLI, mem, 1)
    for iName in range(len(JOB_NAMEs)):
        jobName = JOB_NAMEs[iName]
        batchSize = BatchSizes[iName]
        for iJob in range(NUM_JOBS):
            commonName = str(CPU)+'-'+ str(MEM)+'-'+str(batchSize)+'-'+str(NUM_THREADs)+'-'+str(iJob)

            fNameCpu = jobName+'-cpu-'+commonName
            cpuJobId    = jobName+'-cpu-'+commonName            
            fullCommand = CPU_COMMAND + " --model=" + jobName + " --batch_size="+str(batchSize)+" --num_batches="+str(BatchNUm)+" --num_intra_threads=" + str(NUM_THREADs)
            activeJob = ActiveJob(cpu_usage, 0, 0, cpuJobId, fullCommand,"")
            f_yaml = open(job_folder + '/' + fNameCpu+ ".yaml",'w')   
            f_yaml.write(strPodYaml('job', activeJob, SCHEDULER, False))
            f_yaml.close()

            fNameGpu = jobName+'-gpu-'+ commonName
            gpuJobId    = jobName+'-gpu-'+ commonName           
            fullCommand = GPU_COMMAND + " --model=" + jobName + " --batch_size="+str(batchSize)+" --num_batches="+str(BatchNUm)
            activeJob = ActiveJob(gpu_usage, 0, 0, gpuJobId, fullCommand,"")
            f_yaml = open(job_folder + '/' + fNameGpu+ ".yaml",'w')   
            f_yaml.write(strPodYaml('job', activeJob, SCHEDULER, True))
            f_yaml.close() 

            # submit these two jobs
            strShell = strShell + "kubectl create -f "+ fNameCpu +".yaml 2> " + fNameCpu +".log & \n" 
            strShell = strShell + "kubectl create -f "+ fNameGpu +".yaml 2> " + fNameGpu +".log & \n" 

            # log the pod  
            strLogShell = strLogShell + "kubectl logs job-"+ cpuJobId +"> " + fNameCpu +".log & \n" 
            strLogShell = strLogShell + "kubectl logs job-"+ gpuJobId +"> " + fNameGpu +".log & \n" 

    shellFile = job_folder + "/" + fileName + ".sh"
    f = open(shellFile,'w')

    # strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

    shellLogFile = job_folder + "/log_pod.sh"
    f = open(shellLogFile,'w')

    # strShell = strShell + "wait"
    f.write(strLogShell)        
    f.close()
    os.chmod(shellLogFile, 0700)


def main():
    
    profiling_folder = this_path + "/" + FOLDER  
    try:
        os.stat(profiling_folder)
    except:
        os.mkdir(profiling_folder)        

    job_folder = this_path + "/" + FOLDER 
    shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
    os.mkdir(job_folder)    
    print("======= generate profiling scripts ==============")

    shellProfiling(job_folder, NUM_JOBS, CPU_COMMAND, "beta_mov", STOP_TIME)
   

    print("======= DONE ==============")


if __name__ == "__main__": main()