kubectl create -f alexnet_cpu-0.yaml 2> alexnet_cpu-0.log & 
kubectl create -f alexnet_cpu-1.yaml 2> alexnet_cpu-1.log & 
kubectl create -f alexnet_cpu-2.yaml 2> alexnet_cpu-2.log & 
kubectl create -f alexnet_cpu-3.yaml 2> alexnet_cpu-3.log & 
kubectl create -f alexnet_cpu-4.yaml 2> alexnet_cpu-4.log & 
wait