kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
sleep 5
kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
sleep 5
kubectl --namespace="user1" create -f user1-2.yaml 2> user1-2.log & 