from job import *
import os 
import shutil

JOB_FOLDER = "/jobs"

Gi = 1024*1024*1024

def strUserYaml(username):
    strYaml = ""    
    strYaml = strYaml + "apiVersion: v1" + "\n"
    strYaml = strYaml + "kind: Namespace" + "\n"
    strYaml = strYaml + "metadata:" + "\n"
    strYaml = strYaml + "  name: " + username
    return strYaml



def strPodYaml(username, activeJob, scheduler, isGPU):
    strYaml = ""        
    strYaml = strYaml + "apiVersion: v1" + "\n"
    strYaml = strYaml + "kind: Pod" + "\n"
    strYaml = strYaml + "metadata:" + "\n"
    strYaml = strYaml + "  name: "+username+"-" + str(activeJob.jobId) + "\n"
    strYaml = strYaml + "spec:" + "\n"
    if (scheduler != "kube-scheduler"):
        strYaml = strYaml + "  schedulerName: " + scheduler + "\n"
    strYaml = strYaml + "  containers:" + "\n"
    strYaml = strYaml + "  - name: "+username+"-" + str(activeJob.jobId) + "\n"
    if isGPU:
        strYaml = strYaml + "    image: lenhattan86/ira:gpu" + "\n"
    else:
        strYaml = strYaml + "    image: lenhattan86/ira:cpu" + "\n"
    strYaml = strYaml + "    command:" + "\n"
    strYaml = strYaml + "    - \"/bin/bash\"" + "\n"
    strYaml = strYaml + "    - \"-c\"" + "\n"
    strYaml = strYaml + "    - \"" + activeJob.jobCmd+ "\"" + "\n"
    strYaml = strYaml + "    - \"" + activeJob.seJobCmd+ "\"" + "\n"
    strYaml = strYaml + "    - \"" + str(int(activeJob.usage.MilliCPU))+"," + str(int(activeJob.usage.NvidiaGPU))+","+ str(int(activeJob.usage.Memory/Gi)) + "\"" + "\n"
    strYaml = strYaml + "    - \"" + str(int(activeJob.secUsage.MilliCPU))+"," + str(int(activeJob.secUsage.NvidiaGPU))+","+ str(int(activeJob.secUsage.Memory/Gi)) + "\"" + "\n"
    strYaml = strYaml + "    resources:" + "\n"
    strYaml = strYaml + "      requests:" + "\n"
    strYaml = strYaml + "        alpha.kubernetes.io/nvidia-gpu: " + str(int(activeJob.usage.NvidiaGPU)) + "\n"
    strYaml = strYaml + "        cpu: " + str(float(activeJob.usage.MilliCPU)/1000) + "\n"
    strYaml = strYaml + "        memory: " + str(int(activeJob.usage.Memory/Gi)) + "Gi" + "\n"
    strYaml = strYaml + "      limits:" + "\n"
    strYaml = strYaml + "        alpha.kubernetes.io/nvidia-gpu: " + str(int(activeJob.usage.NvidiaGPU)) + "\n"
    strYaml = strYaml + "        cpu: " + str(float(activeJob.usage.MilliCPU)/1000) + "\n"
    strYaml = strYaml + "        memory: " + str(int(activeJob.usage.Memory/Gi)) + "Gi" + "\n"
    strYaml = strYaml + "    volumeMounts:" + "\n"
    strYaml = strYaml + "    - name: nvidia-driver-384-98" + "\n"
    strYaml = strYaml + "      mountPath: /usr/local/nvidia" + "\n"
    strYaml = strYaml + "      readOnly: true" + "\n"
    strYaml = strYaml + "    - name: libcuda-so" + "\n"
    strYaml = strYaml + "      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so" + "\n"
    strYaml = strYaml + "    - name: libcuda-so-1" + "\n"
    strYaml = strYaml + "      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.1" + "\n"
    strYaml = strYaml + "    - name: libcuda-so-384-98" + "\n"
    strYaml = strYaml + "      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.384.98" + "\n"
    strYaml = strYaml + "      readOnly: true" + "\n"
    strYaml = strYaml + "  restartPolicy: Never" + "\n"
    # strYaml = strYaml + "  restartPolicy: OnFailure" + "\n"
    strYaml = strYaml + "  volumes:" + "\n"
    strYaml = strYaml + "  - name: nvidia-driver-384-98" + "\n"
    strYaml = strYaml + "    hostPath:" + "\n"
    strYaml = strYaml + "      path: /usr/lib/nvidia-384" + "\n"
    strYaml = strYaml + "  - name: libcuda-so" + "\n"
    strYaml = strYaml + "    hostPath:" + "\n"
    strYaml = strYaml + "      path: /usr/lib/x86_64-linux-gnu/libcuda.so" + "\n"
    strYaml = strYaml + "  - name: libcuda-so-1" + "\n"
    strYaml = strYaml + "    hostPath:" + "\n"
    strYaml = strYaml + "      path: /usr/lib/x86_64-linux-gnu/libcuda.so.1" + "\n"
    strYaml = strYaml + "  - name: libcuda-so-384-98" + "\n"
    strYaml = strYaml + "    hostPath:" + "\n"
    strYaml = strYaml + "      path: /usr/lib/x86_64-linux-gnu/libcuda.so.384.98"
    return strYaml
    
def prepareKubernetesJobs(username, scheduler, expFolder, loggedJobs, isQueuedUp):
    this_path = os.path.dirname(os.path.realpath(__file__))
    job_folder = this_path + "/" + expFolder
    try:
        os.stat(job_folder )
    except:
        os.mkdir(job_folder)

    # create user yaml file
    f = open(job_folder + '/' + username + ".yaml",'w')
    f.write(strUserYaml(username))

    f.close()    
    # for each job, create a yaml file
    for jobId in range(len(loggedJobs)):
        activeJob = loggedJobs[jobId]
        isGPU = False
        if activeJob.usage.NvidiaGPU > 0:
            isGPU = True
        f = open(job_folder + '/' + username +"-"+str(jobId) + ".yaml",'w')
        f.write(strPodYaml(username, activeJob, scheduler, isGPU))
        f.close()

    shellFile = job_folder + '/' + username + ".sh"
    f = open(shellFile,'w')
    strShell = ""
    arrivalTime = 0
    # print("num of loggedJobs = "  + str(len(loggedJobs)))
    #         

    for jobId in range(len(loggedJobs)):        
        job = loggedJobs[jobId]
        # print("job "  + str(jobId))
        if isQueuedUp:
            interarrival = 0
            # strShell = strShell + "sleep "+str(interarrival)+"; "
        else:
            interarrival = job.startTime - arrivalTime
            if interarrival > 0:
                interarrival = max(1, interarrival*0.85)
                strShell = strShell + "sleep "+str(interarrival)+"; "

        strShell = strShell + "kubectl --namespace=\""+username+"\" create -f "+ username +"-"+str(jobId) +".yaml 2> " + username +"-"+str(jobId) +".log & \n"
        arrivalTime = job.startTime

    strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)


def mainShell(users,expFolder, stopTime, interval, startTime):
    this_path = os.path.dirname(os.path.realpath(__file__))
    job_folder = this_path + "/" +expFolder
    shutil.rmtree(job_folder, ignore_errors=True)
    os.mkdir(job_folder)
    
    shellFile = job_folder + "/main.sh"
    f = open(shellFile,'w')    
    strShell = ""   

    strShell = strShell + "sudo docker pull lenhattan86/ira:cpu \n"
    strShell = strShell + "sudo docker pull lenhattan86/ira:gpu \n"

    for user in users:                
        strShell = strShell + "kubectl delete pod --all --namespace " + user.username + "\n"

    strShell = strShell + "echo wait.... ; sleep 60 \n"

    ## create namespaces
    for user in users:                
        strShell = strShell + "kubectl create -f " + user.username + ".yaml \n"

    
    
    ## Run the jobs
    for user in users:                
        strShell = strShell + "./" + user.username + ".sh &\n"

    ## Run the monitoring script
    # for user in users:                
        # strShell = strShell + "python ../get_user_info.py --user "+user.username+ \
        # " --interval="+str(interval) + " --stopTime="+str(stopTime)+" --file="+user.username+".csv & \n" 
                      
    strShell = strShell + "sleep "+str(startTime)+"; "    
    strShell = strShell + "python ../get_user_info_timer.py " + \
    " --interval="+str(interval) + " --stopTime="+str(stopTime)+" --file=pods.csv \n"                
    
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)