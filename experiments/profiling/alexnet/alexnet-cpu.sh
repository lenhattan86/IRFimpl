kubectl create -f alexnet-cpu-0.yaml 2> alexnet-cpu-0.log & 
kubectl create -f alexnet-cpu-1.yaml 2> alexnet-cpu-1.log & 
kubectl create -f alexnet-cpu-2.yaml 2> alexnet-cpu-2.log & 
kubectl create -f alexnet-cpu-3.yaml 2> alexnet-cpu-3.log & 
kubectl create -f alexnet-cpu-4.yaml 2> alexnet-cpu-4.log & 
wait