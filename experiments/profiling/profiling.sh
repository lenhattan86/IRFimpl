kubectl create -f vgg16-cpu-16-12-32-16-0.yaml 2> vgg16-cpu-16-12-32-16-0.log & 
kubectl create -f vgg16-gpu-16-12-32-16-0.yaml 2> vgg16-gpu-16-12-32-16-0.log & 
sleep 2 
kubectl create -f vgg16-cpu-16-12-32-16-1.yaml 2> vgg16-cpu-16-12-32-16-1.log & 
kubectl create -f vgg16-gpu-16-12-32-16-1.yaml 2> vgg16-gpu-16-12-32-16-1.log & 
sleep 2 
kubectl create -f vgg16-cpu-16-12-32-16-2.yaml 2> vgg16-cpu-16-12-32-16-2.log & 
kubectl create -f vgg16-gpu-16-12-32-16-2.yaml 2> vgg16-gpu-16-12-32-16-2.log & 
sleep 2 
kubectl create -f googlenet-cpu-16-12-16-16-0.yaml 2> googlenet-cpu-16-12-16-16-0.log & 
kubectl create -f googlenet-gpu-16-12-16-16-0.yaml 2> googlenet-gpu-16-12-16-16-0.log & 
sleep 2 
kubectl create -f googlenet-cpu-16-12-16-16-1.yaml 2> googlenet-cpu-16-12-16-16-1.log & 
kubectl create -f googlenet-gpu-16-12-16-16-1.yaml 2> googlenet-gpu-16-12-16-16-1.log & 
sleep 2 
kubectl create -f googlenet-cpu-16-12-16-16-2.yaml 2> googlenet-cpu-16-12-16-16-2.log & 
kubectl create -f googlenet-gpu-16-12-16-16-2.yaml 2> googlenet-gpu-16-12-16-16-2.log & 
sleep 2 
kubectl create -f alexnet-cpu-16-12-64-16-0.yaml 2> alexnet-cpu-16-12-64-16-0.log & 
kubectl create -f alexnet-gpu-16-12-64-16-0.yaml 2> alexnet-gpu-16-12-64-16-0.log & 
sleep 2 
kubectl create -f alexnet-cpu-16-12-64-16-1.yaml 2> alexnet-cpu-16-12-64-16-1.log & 
kubectl create -f alexnet-gpu-16-12-64-16-1.yaml 2> alexnet-gpu-16-12-64-16-1.log & 
sleep 2 
kubectl create -f alexnet-cpu-16-12-64-16-2.yaml 2> alexnet-cpu-16-12-64-16-2.log & 
kubectl create -f alexnet-gpu-16-12-64-16-2.yaml 2> alexnet-gpu-16-12-64-16-2.log & 
sleep 2 
kubectl create -f inception3-cpu-16-12-16-16-0.yaml 2> inception3-cpu-16-12-16-16-0.log & 
kubectl create -f inception3-gpu-16-12-16-16-0.yaml 2> inception3-gpu-16-12-16-16-0.log & 
sleep 2 
kubectl create -f inception3-cpu-16-12-16-16-1.yaml 2> inception3-cpu-16-12-16-16-1.log & 
kubectl create -f inception3-gpu-16-12-16-16-1.yaml 2> inception3-gpu-16-12-16-16-1.log & 
sleep 2 
kubectl create -f inception3-cpu-16-12-16-16-2.yaml 2> inception3-cpu-16-12-16-16-2.log & 
kubectl create -f inception3-gpu-16-12-16-16-2.yaml 2> inception3-gpu-16-12-16-16-2.log & 
sleep 2 
