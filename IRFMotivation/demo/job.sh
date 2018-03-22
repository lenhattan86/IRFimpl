#!/bin/bash
# ./job.sh username podname cpu gpu memory

username=$1
podname=$2
jobname=$3
cpu=$4
gpu=$5
Gi="Gi"
mem="$6$Gi"


if [ "$jobname" == "alexnet-cpu" ];
then  
  CMD="python tf_cnn_benchmarks.py --device=cpu --model=$job --data_format=NHWC --batch_size=32 --num_batches=100"
elif [ "$jobname" == "alexnet-gpu" ];
then
  CMD="python tf_cnn_benchmarks.py --device=gpu --model=$job --data_format=NHWC --batch_size=32 --num_batches=100"
elif [ "$jobname" == "s-linear-cpu" ];
then
  CMD="python linear_regression_cpu.py"
elif [ "$jobname" == "s-linear-gpu" ];
then
  CMD="python linear_regression.py"
else
  echo "no job detected."
fi

# create new jobs
echo "apiVersion: v1
kind: Pod
metadata:
  name: $podname
spec:
  containers:
  - name: $podname
    image: swiftdiaries/bench
    command:
    - \"/bin/bash\"
    - \"-c\"
    - \"$CMD\"  
    resources:
      requests:
        alpha.kubernetes.io/nvidia-gpu: $gpu
        cpu: $cpu
        memory: $mem
      limits:
        alpha.kubernetes.io/nvidia-gpu: $gpu
        cpu: $cpu
        memory: $mem
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
" > ./jobs/$podname.yaml
    
FULL_COMMAND="kubectl --namespace=\"$username\" create -f ./jobs/$podname.yaml"        
>&2 echo "Starting pod $podname."
echo $FULL_COMMAND
#(TIMEFORMAT='%R'; time $FULL_COMMAND 2>./logs/$podname.log) 2> ./time/$podname.time