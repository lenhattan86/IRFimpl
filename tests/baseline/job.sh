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
  CMD="python /benchmarks/scripts/tf_benchmarks/tf_cnn_benchmarks.py --device=cpu --model=alexnet --data_format=NHWC --batch_size=32 --num_batches=100"
elif [ "$jobname" == "alexnet-gpu" ];
then
  CMD="python tf_cnn_benchmarks.py --device=gpu --model=alexnet --data_format=NHWC --batch_size=32 --num_batches=100"
elif [ "$jobname" == "s-linear-cpu" ];
then
  CMD="python linear_regression_cpu.py"
elif [ "$jobname" == "s-linear-gpu" ];
then
  CMD="python linear_regression.py"
else
  CMD="$jobname"
fi

cuda="384" # 375
cuda_version="384-111"
cuda_suffix="384.111" 

# create new jobs
echo "apiVersion: v1
kind: Pod
metadata:
  name: $podname
spec:
  containers:
  - name: $podname
    image: lenhattan86/bench
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
    - name: nvidia-driver-$cuda_version
      mountPath: /usr/local/nvidia
      readOnly: true
    - name: libcuda-so
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so
    - name: libcuda-so-1
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.1
    - name: libcuda-so-$cuda_version
      mountPath: /usr/lib/x86_64-linux-gnu/libcuda.so.$cuda_suffix
      readOnly: true
  restartPolicy: Never
  volumes:
  - name: nvidia-driver-$cuda_version
    hostPath:
      path: /usr/lib/nvidia-$cuda
  - name: libcuda-so
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so
  - name: libcuda-so-1
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so.1
  - name: libcuda-so-$cuda_version
    hostPath:
      path: /usr/lib/x86_64-linux-gnu/libcuda.so.$cuda_suffix
" > ./jobs/$podname.yaml
    
kubectl --namespace="$username" create -f ./jobs/$podname.yaml &
./log.sh $username $podname