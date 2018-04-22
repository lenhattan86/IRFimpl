kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
wait