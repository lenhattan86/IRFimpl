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
  numberOfCoresStart=1
else
  numberOfCoresStart=$1
fi
if [ -z "$2" ]
then
  numberOfCoreEnd=3
else
  numberOfCoreEnd=$2
fi


#FULL_COMMAND="kubectl --namespace=\"user1\" create -f ./jobs/vgg-gpu-job.yaml"

if [ -z "$3" ]
then
  job="vgg16"
  #job="alexnet"
  #job="resnet50"
  #job="inception3"
else
  job="$3"
fi

jobName="$job-cpu-job"

for i in $(seq $numberOfCoresStart $numberOfCoreEnd);
do  
    # create new jobs
    echo "apiVersion: v1
kind: Pod
metadata:
  name: tensorflow-$job-cpu$i
spec:
  containers:
  - name: tensorflow-$job-cpu
    image: swiftdiaries/bench
    command:
    - \"/bin/bash\"
    - \"-c\"
    - \"python tf_cnn_benchmarks.py --device=cpu --model=$job --data_format=NHWC --batch_size=16 --num_intra_threads=$i --num_batches=1000\"  
    resources:
      requests:
        alpha.kubernetes.io/nvidia-gpu: 1
        cpu: $i
        memory: 16Gi
      limits:
        alpha.kubernetes.io/nvidia-gpu: 1
        cpu: $i
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
	  (TIMEFORMAT='%R'; time $FULL_COMMAND 2>./logs/application$i.log) 2> ./time/$i.time &
done
