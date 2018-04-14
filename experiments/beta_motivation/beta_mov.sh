kubectl create -f vgg11-cpu-16-12-32-16-0.yaml 2> vgg11-cpu-16-12-32-16-0.log & 
kubectl create -f vgg11-gpu-16-12-32-16-0.yaml 2> vgg11-gpu-16-12-32-16-0.log & 
kubectl create -f vgg16-cpu-16-12-32-16-0.yaml 2> vgg16-cpu-16-12-32-16-0.log & 
kubectl create -f vgg16-gpu-16-12-32-16-0.yaml 2> vgg16-gpu-16-12-32-16-0.log & 
