sleep 5 
kubectl create -f vgg16-cpu-19-64-256-32-0.yaml 2> vgg16-cpu-19-64-256-32-0.log 
sleep 5 
kubectl create -f vgg16-cpu-19-64-128-64-0.yaml 2> vgg16-cpu-19-64-128-64-0.log 
sleep 5 
kubectl create -f vgg16-cpu-19-64-64-128-0.yaml 2> vgg16-cpu-19-64-64-128-0.log 
sleep 5 
kubectl create -f vgg16-cpu-19-64-32-256-0.yaml 2> vgg16-cpu-19-64-32-256-0.log 
sleep 5 
kubectl create -f alexnet-cpu-19-64-256-32-0.yaml 2> alexnet-cpu-19-64-256-32-0.log 
sleep 5 
kubectl create -f alexnet-cpu-19-64-128-64-0.yaml 2> alexnet-cpu-19-64-128-64-0.log 
sleep 5 
kubectl create -f alexnet-cpu-19-64-64-128-0.yaml 2> alexnet-cpu-19-64-64-128-0.log 
sleep 5 
kubectl create -f alexnet-cpu-19-64-32-256-0.yaml 2> alexnet-cpu-19-64-32-256-0.log 
