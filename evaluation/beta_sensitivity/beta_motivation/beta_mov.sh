kubectl create -f lenet-cpu-16-12-8192-16-0.yaml 2> lenet-cpu-16-12-8192-16-0.log & 
kubectl create -f lenet-gpu-16-12-8192-16-0.yaml 2> lenet-gpu-16-12-8192-16-0.log & 
kubectl create -f lenet-cpu-16-12-8192-16-1.yaml 2> lenet-cpu-16-12-8192-16-1.log & 
kubectl create -f lenet-gpu-16-12-8192-16-1.yaml 2> lenet-gpu-16-12-8192-16-1.log & 
kubectl create -f lenet-cpu-16-12-8192-16-2.yaml 2> lenet-cpu-16-12-8192-16-2.log & 
kubectl create -f lenet-gpu-16-12-8192-16-2.yaml 2> lenet-gpu-16-12-8192-16-2.log & 
