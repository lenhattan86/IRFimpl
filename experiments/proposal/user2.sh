sleep 150
# kill user 1 jobs
kubectl delete -f user1-0.yaml 
kubectl delete -f user1-1.yaml 
kubectl delete -f user1-2.yaml 
kubectl delete -f user1-3.yaml 

# submit user 2 jobs
kubectl create -f user2-0.yaml 
kubectl create -f user2-1.yaml 
kubectl create -f user2-2.yaml 
kubectl create -f user2-3.yaml 

# resubmit user 1 jobs
sleep 40
kubectl create -f user1-0.yaml 
kubectl create -f user1-1.yaml 
kubectl create -f user1-2.yaml 
kubectl create -f user1-3.yaml 