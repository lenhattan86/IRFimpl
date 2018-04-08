import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *

# generate jobs

# parameters
# number of cpus
# Memory size
# batch-size 
# num. of batches

CPU_4_GPU = 1 # GPU job
GPU = 1
CPU = 3 # CPU job

CPUs               = [1, 2, 3, 4] # vs. 1 GPU


MEM_GBs            = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
BATCH_SIZE         = [16, 32, 64, 128, 256]
BATCH_SIZE_MIN_MEM = [3, 6, 9, 12]
NUM_OF_BATCHES     = [3, 6, 9, 12]

MAIN_COMMAND

# 

NUM_JOBS = 1
STOP_TIME = 10000
FOLDER = "gen_prof_jobs"

this_path = os.path.dirname(os.path.realpath(__file__))

def shellProfiling(job_folder, job_number, cpuResource, cpuCmd, gpuResource, gpuCmd, job_name,stopTime):    
    shellFile = job_folder + "/profiling.sh"
    f = open(shellFile,'w')
    strShell = ""   

    strShell = strShell + "kubectl delete pods --all --namespace=default \n"
    strShell = strShell + "echo wait... \n"
    strShell = strShell + "sleep 60 \n"
    strShell = strShell + "sudo docker pull lenhattan86/cpu \n"
    strShell = strShell + "sudo docker pull lenhattan86/gpu \n"
    
    strShell = strShell + "python ../../get_user_info_timer.py --user=default" \
        " --interval="+str(1) + " --stopTime="+str(stopTime)+" --file="+job_name+".csv & pythonScript=$! \n"  

    ## create CPU jobs
    shellJobs(job_folder, job_number, cpuResource, cpuCmd, job_name+"-cpu")
    ## create GPU jobs
    shellJobs(job_folder, job_number, gpuResource, gpuCmd, job_name+"-gpu")

    strShell = strShell + "./" +job_name+"-cpu" + ".sh & cpuScript=$! \n"               
    strShell = strShell + "./" + job_name+"-gpu"+ ".sh & gpuScript=$!\n"

    strShell = strShell + "wait"    
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def shellJobs(job_folder, job_number, job_resource, cmd, fileName):
    isGPU = False
    ## create yaml files
    for i in range(job_number):
        usage = Resource(job_resource.MilliCPU, job_resource.Memory, job_resource.NvidiaGPU)
        activeJob = ActiveJob(usage, 0, 0, fileName+'-'+str(i),cmd)
        f_yaml = open(job_folder + '/' + fileName + '-'+str(i) + ".yaml",'w')
        if job_resource.NvidiaGPU > 0:
            isGPU = True
        f_yaml.write(strPodYaml('job', activeJob, 'kube-scheduler', isGPU))
        f_yaml.close()        

    shellFile = job_folder + "/" + fileName + ".sh"
    f = open(shellFile,'w')
    strShell = ""       

    ## submit yaml files
    for i in range(job_number):                        
        strShell = strShell + "kubectl create -f "+ fileName + '-'+str(i) +".yaml 2> " + fileName + '-'+str(i) +".log & \n"        

    # strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def main():
    
    profiling_folder = this_path + "/" + FOLDER  
    try:
        os.stat(profiling_folder)
    except:
        os.mkdir(profiling_folder)        

    job_folder = this_path + "/" + FOLDER + "/logs"
    shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
    os.mkdir(job_folder)    
    print("======= generate profiling scripts ==============")

    for mem in range(MEM_GBs):        
        cpu_res = Resource(CPU, mem, 0)
        gpu_res = Resource(CPU_4_GPU, mem, GPU)
        shellProfiling(job_folder, NUM_JOBS, cpu_res, CPU_COMMAND, gpu_res, GPU_COMMAND, JOB_NAME, STOP_TIME)

    print("======= DONE ==============")

if __name__ == "__main__": main()