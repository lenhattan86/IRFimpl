#!/bin/bash
userid="user1 user2";
timer=5
isCreatNameSpace=true
if $isCreatNameSpace
then
  for user in $userid; do
	  kubectl create -f ./namespaces/$user.yaml
  done	
fi

mkdir logs
mkdir time

if [ -z "$1" ]
then
  numberOfJobs=1
else
  numberOfJobs=$1
fi

if [ -z "$2" ]
then
  gpu_fraction=0.19
else
  gpu_fraction=$2
fi

if [ -z "$3" ]
then
  #job="vgg16"
  job="alexnet"
else
  job="$3"
fi

#FULL_COMMAND="kubectl --namespace=\"user1\" create -f ./jobs/vgg-gpu-job.yaml"


jobName="$job-cpu-job"

singleCmd="python tf_cnn_benchmarks.py --device=gpu --model=$job --data_format=NHWC --batch_size=16 --num_batches=1000 --gpu_mem_fraction=$gpu_fraction"
COMMAND="echo start... "
for i in $(seq 1 $numberOfJobs);
do  
  COMMAND="$COMMAND & $singleCmd"
#  COMMAND="$singleCmd"
done
#COMMAND="$COMMAND"
#echo $COMMAND

# create new jobs
echo "apiVersion: v1
kind: Pod
metadata:
  name: tensorflow-$job-gpu$numberOfJobs
spec:
  containers:
  - name: tensorflow-$job-gpu
    image: swiftdiaries/bench
    command:
    - \"/bin/bash\"
    - \"-c\"
    - \"$COMMAND\"  
    resources:
      requests:
        alpha.kubernetes.io/nvidia-gpu: 1
        cpu: 1
        memory: 16Gi
      limits:
        alpha.kubernetes.io/nvidia-gpu: 1
        cpu: 1
        memory: 16Gi
    volumeMounts:
    - name: nvidia-driver-375-82
      mountPath: /usr/local/nvidia
      readOnly: true
    - name: libcuda-so
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so
    - name: libcuda-so-1
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.1
    - name: libcuda-so-375-82
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82
      readOnly: true
  restartPolicy: Never
  volumes:
  - name: nvidia-driver-375-82
    hostPath:
      path: /usr/lib/nvidia-375
  - name: libcuda-so
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so
  - name: libcuda-so-1
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so.1
  - name: libcuda-so-375-82
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so.375.82
    " > ./jobs/$jobName$i.yaml
    
FULL_COMMAND="kubectl create -f ./jobs/$jobName$i.yaml"        
>&2 echo "Starting job $i."
(TIMEFORMAT='%R'; time $FULL_COMMAND 2>./logs/application$i.log) 2> ./time/$i.time
