kubectl create -f alexnet_gpu-0.yaml 2> alexnet_gpu-0.log & 
kubectl create -f alexnet_gpu-1.yaml 2> alexnet_gpu-1.log & 
kubectl create -f alexnet_gpu-2.yaml 2> alexnet_gpu-2.log & 
kubectl create -f alexnet_gpu-3.yaml 2> alexnet_gpu-3.log & 
kubectl create -f alexnet_gpu-4.yaml 2> alexnet_gpu-4.log & 
wait