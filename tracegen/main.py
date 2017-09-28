# this program create list of jobs for a single user
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

# parameters
mu, sigma = 0, 0.1
nUsers = 2;
nJobs = 3;
sleepTime = np.random.normal(mu, sigma, nJobs)
jobNames = ["alexnet"]
username = "userA"
device="cpu"

cpuDemands=[2]
gpuDemands=[1]
memDemands=[1]

## constants
batchSize=32

## main code
fileUser = open(username+".sh","w")
directory= username
# create folder for username
try:
    os.stat(directory)
    shutil.rmtree(directory)
except:
    print("delete the director " + directory)

os.mkdir(directory)

for i in range(nJobs):
    # create yaml file
    fileYamlName = "job_" +str(i)+ ".yaml"
    fileYaml = open(directory + "/" + fileYamlName,"w")
    fileYaml.write("apiVersion: v1")
    fileYaml.write("kind: Pod")
    fileYaml.write("metadata:")
    fileYaml.write("  name: tensorflow-alexnet-cpu")
    fileYaml.write("spec:")
    fileYaml.write("  containers:")
    fileYaml.write("  - name: tensorflow-alexnet-cpu")
    fileYaml.write("    image: swiftdiaries/bench")
    fileYaml.write("    command:")
    fileYaml.write("    - \"/bin/bash\"")
    fileYaml.write("    - \"-c\"")
    fileYaml.write("    - \"python tf_cnn_benchmarks.py --device="+device+" --model="+jobNames[i%len(jobNames)]+" --data_format=NHWC --batch_size="+str(batchSize)+"\"")
    fileYaml.write("    resources:")
    fileYaml.write("      requests:")
    fileYaml.write("        cpu: 40")
    fileYaml.write("      limits:")
    fileYaml.write("        cpu: 40")
    fileYaml.write("    volumeMounts:")
    fileYaml.write("    - name: nvidia-driver-375-82")
    fileYaml.write("      mountPath: /usr/local/nvidia")
    fileYaml.write("      readOnly: true")
    fileYaml.write("    - name: libcuda-so")
    fileYaml.write("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so")
    fileYaml.write("    - name: libcuda-so-1")
    fileYaml.write("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.1")
    fileYaml.write("    - name: libcuda-so-375-82")
    fileYaml.write("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82")
    fileYaml.write("      readOnly: true")
    fileYaml.write("  restartPolicy: Never")
    fileYaml.write("  volumes:")
    fileYaml.write("  - name: nvidia-driver-375-82")
    fileYaml.write("    hostPath:")
    fileYaml.write("      path: /usr/lib/nvidia-375")
    fileYaml.write("  - name: libcuda-so")
    fileYaml.write("    hostPath:")
    fileYaml.write("      path: /usr/lib/x86_64-linux-gnu/libcuda.so")
    fileYaml.write("  - name: libcuda-so-1")
    fileYaml.write("    hostPath:")
    fileYaml.write("      path: /usr/lib/x86_64-linux-gnu/libcuda.so.1")
    fileYaml.write("  - name: libcuda-so-375-82")
    fileYaml.write("    hostPath:")
    fileYaml.write("      path: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82")
    fileYaml.close()

    # create job file
    jobFileName="job"+str(i)+".sh";
    fileJob = open(directory +"/"+jobFileName,"w")
    fileJob.write("kubectl --namespace=\""+username+"\" create -f ./"+directory+"/"+fileYamlName)

    # add job shell to the file
    fileUser.write("sleep "+str(sleepTime.item(i)))
    fileUser.write(directory + "/" +jobFileName +" &")

fileUser.close()



