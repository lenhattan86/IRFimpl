from job import *
import os 
import shutil

JOB_FOLDER = "/jobs"

def strUserYaml(username):
    strYaml = ""    
    strYaml = strYaml + "apiVersion: v1" + "\n"
    strYaml = strYaml + "kind: Namespace" + "\n"
    strYaml = strYaml + "metadata:" + "\n"
    strYaml = strYaml + "  name: " + username
    return strYaml
Gi = 1024*1024*1024
def strPodYaml(username, activeJob):
    strYaml = ""        
    strYaml = strYaml + "apiVersion: v1" + "\n"
    strYaml = strYaml + "kind: Pod" + "\n"
    strYaml = strYaml + "metadata:" + "\n"
    strYaml = strYaml + "  name: "+username+"-" + str(activeJob.jobId) + "\n"
    strYaml = strYaml + "spec:" + "\n"
    strYaml = strYaml + "  schedulerName: my-scheduler"
    strYaml = strYaml + "  containers:" + "\n"
    strYaml = strYaml + "  - name: "+username+"-" + str(activeJob.jobId) + "\n"
    strYaml = strYaml + "    image: lenhattan86/bench" + "\n"
    strYaml = strYaml + "    command:" + "\n"
    strYaml = strYaml + "    - \"/bin/bash\"" + "\n"
    strYaml = strYaml + "    - \"-c\"" + "\n"
    strYaml = strYaml + "    - \"" + activeJob.jobCmd+ "\"" + "\n"
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
    
def prepareKubernetesJobs(username, loggedJobs):
    this_path = os.path.dirname(os.path.realpath(__file__))
    job_folder = this_path + JOB_FOLDER
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
        f = open(job_folder + '/' + username +"-"+str(jobId) + ".yaml",'w')
        f.write(strPodYaml(username, activeJob))
        f.close()

    shellFile = job_folder + '/' + username + ".sh"
    f = open(shellFile,'w')
    strShell = ""
    arrivalTime = 0
    # print("num of loggedJobs = "  + str(len(loggedJobs)))
    #         
    strShell = strShell + "kubectl create -f " + username + ".yaml \n"
    strShell = strShell + "sleep 30 \n"

    for jobId in range(len(loggedJobs)):        
        job = loggedJobs[jobId]
        # print("job "  + str(jobId))
        interarrival = job.startTime - arrivalTime
        if (interarrival>0):            
            strShell = strShell + "sleep 1; "        
        strShell = strShell + "kubectl --namespace=\""+username+"\" create -f "+ username +"-"+str(jobId) +".yaml 2> " + username +"-"+str(jobId) +".log & \n"
        arrivalTime = job.startTime
    strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)


def mainShell(users):
    this_path = os.path.dirname(os.path.realpath(__file__))
    job_folder = this_path + JOB_FOLDER
    shutil.rmtree(job_folder, ignore_errors=True)
    os.mkdir(job_folder)
    
    shellFile = job_folder + "/main.sh"
    f = open(shellFile,'w')
    strShell = ""
    # print("num of loggedJobs = "  + str(len(loggedJobs)))
    
    for user in users:                
        strShell = strShell + "./" + user.username + ".sh &\n"
        
    strShell = strShell + "wait"
    f.write(strShell)        
    f.close()
    os.chmod(shellFile, 0700)