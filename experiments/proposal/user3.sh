sleep 350

# kill user 1 jobs
kubectl delete -f user1-0.yaml 
kubectl delete -f user1-1.yaml 
kubectl delete -f user1-2.yaml 
kubectl delete -f user1-3.yaml 

# submit user 3 jobs
kubectl create -f user3-0.yaml 
kubectl create -f user3-1.yaml 
kubectl create -f user3-2.yaml 
kubectl create -f user3-3.yaml 

# resubmit user 1 jobs
sleep 40
kubectl create -f user1-0.yaml 
kubectl create -f user1-1.yaml 
kubectl create -f user1-2.yaml 
kubectl create -f user1-3.yaml 