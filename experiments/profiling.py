import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *


NUM_JOBS = 5

FOLDER = "profiling"
GI = 1024*1024*1024
CPU_cpu = 23*1000
CPU_mem = 1*GI
CPU_gpu = 0

GPU_cpu = 0.1 *1000
GPU_mem = 1 * GI
GPU_gpu = 1

JOB_NAME = "alexnet"
CPU_COMMAND = "python tf_cnn_benchmarks.py --device=cpu --model="+JOB_NAME+" --data_format=NHWC --batch_size=16 --num_batches=100 --num_intra_threads=23 "
GPU_COMMAND = "python tf_cnn_benchmarks.py --device=gpu --model="+JOB_NAME+" --batch_size=16 --num_batches=100 --num_gpus=1"

this_path = os.path.dirname(os.path.realpath(__file__))

def shellProfiling(job_folder, job_number, cpuResource, cpuCmd, gpuResource, gpuCmd, job_name):    
    shellFile = job_folder + "/profiling.sh"
    f = open(shellFile,'w')
    strShell = ""   

    strShell = strShell + "python ../../get_user_info.py --user=default" \
        " --interval="+str(1) + " --stopTime=-1 --file="+job_name+".csv & \n"  

    ## create CPU jobs
    shellJobs(job_folder, job_number, cpuResource, cpuCmd, job_name+"-cpu")
    ## create GPU jobs
    shellJobs(job_folder, job_number, gpuResource, gpuCmd, job_name+"-gpu")

    strShell = strShell + "./" +job_name+"-cpu" + ".sh &\n"               
    strShell = strShell + "./" + job_name+"-gpu"+ ".sh &\n"

    strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def shellJobs(job_folder, job_number, job_resource, cmd, fileName):
    
    ## create yaml files
    for i in range(job_number):
        usage = Resource(job_resource.MilliCPU, job_resource.Memory, job_resource.NvidiaGPU)
        activeJob = ActiveJob(usage, 0, 0, fileName+'-'+str(i),cmd)
        f_yaml = open(job_folder + '/' + fileName + '-'+str(i) + ".yaml",'w')
        f_yaml.write(strPodYaml('job', activeJob, 'kube-scheduler'))
        f_yaml.close()        

    shellFile = job_folder + "/" + fileName + ".sh"
    f = open(shellFile,'w')
    strShell = ""       

    ## submit yaml files
    for i in range(job_number):                        
        strShell = strShell + "kubectl create -f "+ fileName + '-'+str(i) +".yaml 2> " + fileName + '-'+str(i) +".log & \n"        

    strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def main():
    
    profiling_folder = this_path + "/" + FOLDER  
    try:
        os.stat(profiling_folder)
    except:
        os.mkdir(profiling_folder)        

    job_folder = this_path + "/" + FOLDER + "/" + JOB_NAME    
    shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
    os.mkdir(job_folder)    
    print("======= generate profiling scripts ==============")
    cpu_res = Resource(CPU_cpu, CPU_mem, CPU_gpu)
    gpu_res = Resource(GPU_cpu, GPU_mem, GPU_gpu)

    shellProfiling(job_folder, NUM_JOBS, cpu_res, CPU_COMMAND, gpu_res, GPU_COMMAND, JOB_NAME)

    print("======= DONE ==============")


if __name__ == "__main__": main()