# this program create list of jobs for a single user
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

class ofile(file):
    #subclass file to have a more convienient use of writeline
    def __init__(self, name, mode = 'r'):
        self = file.__init__(self, name, mode)

    def wl(self, string):
        self.writelines(string + '\n')
        return None

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)


# parameters
mu, sigma = 10, 4
nUsers = 2;
nJobs = 3;
sleepTime = abs(np.random.normal(mu, sigma, nJobs))
jobNames = ["alexnet"]
username = "userA"
device="cpu"

cpuDemands=[2]
gpuDemands=[1]
memDemands=[1]

commands = ["tf_cnn_benchmarks.py"]

## constants
batchSize=32

## main code
fileName=username+".sh";
fileUser = ofile(fileName,"w")
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
    fileYaml = ofile(directory + "/" + fileYamlName,"w")
    fileYaml.wl("apiVersion: v1")
    fileYaml.wl("kind: Pod")
    fileYaml.wl("metadata:")
    fileYaml.wl("  name: tensorflow-alexnet-cpu")
    fileYaml.wl("spec:")
    fileYaml.wl("  containers:")
    fileYaml.wl("  - name: tensorflow-alexnet-cpu")
    fileYaml.wl("    image: swiftdiaries/bench")
    fileYaml.wl("    command:")
    fileYaml.wl("    - \"/bin/bash\"")
    fileYaml.wl("    - \"-c\"")
    fileYaml.wl("    - \"python "+commands[i%len(commands)]+" --device="+device+" --model="+jobNames[i%len(jobNames)]+" --data_format=NHWC --batch_size="+str(batchSize)+"\"")
    fileYaml.wl("    resources:")
    fileYaml.wl("      requests:")
    fileYaml.wl("        cpu: 1")
    fileYaml.wl("      limits:")
    fileYaml.wl("        cpu: 1")
    fileYaml.wl("    volumeMounts:")
    fileYaml.wl("    - name: nvidia-driver-375-82")
    fileYaml.wl("      mountPath: /usr/local/nvidia")
    fileYaml.wl("      readOnly: true")
    fileYaml.wl("    - name: libcuda-so")
    fileYaml.wl("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so")
    fileYaml.wl("    - name: libcuda-so-1")
    fileYaml.wl("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.1")
    fileYaml.wl("    - name: libcuda-so-375-82")
    fileYaml.wl("      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82")
    fileYaml.wl("      readOnly: true")
    fileYaml.wl("  restartPolicy: Never")
    fileYaml.wl("  volumes:")
    fileYaml.wl("  - name: nvidia-driver-375-82")
    fileYaml.wl("    hostPath:")
    fileYaml.wl("      path: /usr/lib/nvidia-375")
    fileYaml.wl("  - name: libcuda-so")
    fileYaml.wl("    hostPath:")
    fileYaml.wl("      path: /usr/lib/x86_64-linux-gnu/libcuda.so")
    fileYaml.wl("  - name: libcuda-so-1")
    fileYaml.wl("    hostPath:")
    fileYaml.wl("      path: /usr/lib/x86_64-linux-gnu/libcuda.so.1")
    fileYaml.wl("  - name: libcuda-so-375-82")
    fileYaml.wl("    hostPath:")
    fileYaml.wl("      path: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82")
    fileYaml.close()

    # create job file
    jobFileName="job"+str(i)+".sh";
    fileJob = ofile(directory +"/"+jobFileName,"w")
    fileJob.wl("kubectl --namespace=\""+username+"\" create -f ./"+directory+"/"+fileYamlName)
    fileJob.close()
    make_executable(directory +"/"+jobFileName)
    # add job shell to the file
    fileUser.wl("sleep "+str(sleepTime.item(i)))
    fileUser.wl(directory +"/"+jobFileName +" &")

fileUser.close()
make_executable(fileName)
