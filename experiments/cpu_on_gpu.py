# this file generate the script to evaluate the impact of cpu on GPU jobs.
import os 
import allocator
from job import *
from user import *
from demand import *
from resource import *
from allocator import *
from kubernetes import *



JOB_NAME = "alexnet"
benchmarks = "tf_cnn_benchmarks.py"

#CPU_COMMAND = "python tf_cnn_benchmarks.py --device=cpu --model="+JOB_NAME+" --data_format=NHWC --batch_size=16 --num_batches=400 --num_intra_threads=22 "
GPU_COMMAND = "python tf_cnn_benchmarks.py --device=gpu --model="+JOB_NAME+" --batch_size=16 --num_batches=200 --num_gpus=1"
CPUs = [0.1, 0.2, 0.4, 0.8, 1.0, 1.5, 2.0, 3.0]
##########################

MILLI=1000
NUM_JOBS = 5
STOP_TIME = 36000
FOLDER = "cpu_on_gpu"
GI = 1024*1024*1024
MEM = 3*GI
SCHEDULER = "kube-scheduler"
this_path = os.path.dirname(os.path.realpath(__file__))

def shellProfiling(job_folder, job_number, gpuCmd, job_name, stopTime):    
    shellFile = job_folder + "/profiling.sh"
    f = open(shellFile,'w')
    strShell = ""   

    strShell = strShell + "kubectl delete pods --all --namespace=default \n"
    strShell = strShell + "echo wait... \n"
    strShell = strShell + "sleep 60 \n"
    
    strShell = strShell + "sudo docker pull lenhattan86/gpu \n"
    
    strShell = strShell + "python ../../get_user_info_timer.py " \
        " --interval="+str(1) + " --stopTime="+str(stopTime)+" --file="+job_name+".csv & pythonScript=$! \n"  

    ## create GPU jobs
    shellJobs(job_folder, job_number, gpuCmd, job_name)

    getLogScript(job_folder, NUM_JOBS, job_name)

    strShell = strShell + "./" +job_name+".sh & cpuScript=$! \n"               

    strShell = strShell + "wait"    
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def shellJobs(job_folder, job_number, cmd, fileName):
    isGPU = True
    ## create yaml files
    strShell = ""
    for i in range(job_number):
        for cpu in CPUs:
            miliCPU = cpu*MILLI
            gpu_res = Resource(miliCPU, MEM, 1)
            fName = fileName+'-'+str(cpu)+'-'+str(i)
            jobId = fileName+'-'+str(int(cpu*10))+'-'+str(i)
            activeJob = ActiveJob(gpu_res, 0, 0, jobId,cmd)
            f_yaml = open(job_folder + '/' + fName+ ".yaml",'w')   
            f_yaml.write(strPodYaml('job', activeJob, SCHEDULER, isGPU))
            f_yaml.close()      
            # submit this job  
            strShell = strShell + "kubectl create -f "+ fName +".yaml 2> " + fName +".log & \n" 

    shellFile = job_folder + "/" + fileName + ".sh"
    f = open(shellFile,'w')


    # strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def getLogScript(job_folder, job_number, job_name):
    strShell = ""
    for i in range(job_number):
        for cpu in CPUs:
            fName = job_name+'-'+str(cpu)+'-'+str(i)
            jobId = job_name+'-'+str(int(cpu*10))+'-'+str(i)

            # log the pod  
            strShell = strShell + "kubectl logs job-"+ jobId +"> " + fName +".log & \n" 

    shellFile = job_folder + "/log_pod.sh"
    f = open(shellFile,'w')


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

    job_folder = this_path + "/" + FOLDER + "/" + JOB_NAME    
    shutil.rmtree(job_folder, ignore_errors=True) # delete previous folder.
    os.mkdir(job_folder)    
    print("======= generate profiling scripts ==============")

    shellProfiling(job_folder, NUM_JOBS, GPU_COMMAND, JOB_NAME, STOP_TIME)
   

    print("======= DONE ==============")


if __name__ == "__main__": main()