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

NUM_JOBS = 1
NUM_THREADs = [19, 38]
# JOB_NAMEs   = ['vgg16', 'lenet', 'googlenet', 'alexnet',  'resnet50', 'inception3', 'overfeat']
JOB_NAMEs   = ['vgg16']
# JOB_NAMEs   = ['alexnet']
BatchNum    = 50
batchSize   = 32
CPUs = [1, 2, 4, 6, 8, 12, 15, 19]
MEM = 12
CPU_COMMAND = "python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --num_warmup_batches=0 "
MILLI=1000

##########################
STOP_TIME = -1
FOLDER = "prof_cpu"
GI = 1024*1024*1024
SCHEDULER = "kube-scheduler"
this_path = os.path.dirname(os.path.realpath(__file__))

def shellProfiling(job_folder, job_number, gpuCmd, exp_name, stopTime):    
    shellFile = job_folder + "/main.sh"
    f = open(shellFile,'w')
    strShell = ""   

    # strShell = strShell + "kubectl delete pods --all --namespace=default --grace-period=0 --force \n"
    strShell = strShell + "kubectl delete pods --all --namespace=default \n"
    strShell = strShell + "echo wait... \n"
    strShell = strShell + "sleep 60 \n"
    
    strShell = strShell + "sudo docker pull lenhattan86/gpu \n"
    strShell = strShell + "sudo docker pull lenhattan86/cpu \n"

    ## create GPU jobs
    shellJobs(job_folder, job_number, gpuCmd, exp_name)

    strShell = strShell + "./" +exp_name+".sh & cpuScript=$! \n"               

    strShell = strShell + "python ../get_user_info_timer.py " \
        " --interval="+str(1) + " --stopTime="+str(stopTime)+" --file=pods.csv &\n"  

    strShell = strShell + "wait $cpuScript \n"  

    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)

def shellJobs(job_folder, job_number, cmd, fileName):
    ## create yaml files
    strShell = ""
    strLogShell = ""
    for jobName in JOB_NAMEs:
        for NUM_THREAD in NUM_THREADs:
            for CPU in CPUs:
                cpu = CPU*MILLI
                cpu_usage = Resource(cpu, MEM*GI, 0)
                gpu_usage = Resource(1, MEM*GI, 1)
                for iJob in range(NUM_JOBS):
                    commonName = str(CPU)+'-'+ str(MEM)+'-' + str(NUM_THREAD)+'-'  +str(iJob)
                    cpuFullCommand = CPU_COMMAND + " --model=" + jobName + " --batch_size="+str(batchSize)+" --num_intra_threads=" + str(NUM_THREAD) +" --num_batches="+str(BatchNum)

                    fNameCpu = jobName+'-cpu-'+commonName
                    cpuJobId    = jobName+'-cpu-'+commonName            
                    
                    activeJob = ActiveJob(cpu_usage, gpu_usage, 0, 0, cpuJobId, cpuFullCommand,'')
                    f_yaml = open(job_folder + '/' + fNameCpu+ ".yaml",'w')   
                    f_yaml.write(strPodYaml('job', activeJob, SCHEDULER, False))
                    f_yaml.close()

                    # submit these two jobs
                    strShell = strShell + "sleep 5 \n" 
                    strShell = strShell + "kubectl create -f "+ fNameCpu +".yaml 2> " + fNameCpu +".log \n"                     
                    strLogShell = strLogShell + "kubectl logs job-"+ cpuJobId +"> " + fNameCpu +".log \n" 
                    
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

    shellProfiling(job_folder, NUM_JOBS, CPU_COMMAND, "jobs", STOP_TIME)
   

    print("======= DONE ==============")


if __name__ == "__main__": main()