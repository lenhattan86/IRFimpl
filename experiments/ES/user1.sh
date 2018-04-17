kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
kubectl --namespace="user1" create -f user1-2.yaml 2> user1-2.log & 
kubectl --namespace="user1" create -f user1-3.yaml 2> user1-3.log & 
sleep 162.35; kubectl --namespace="user1" create -f user1-4.yaml 2> user1-4.log & 
kubectl --namespace="user1" create -f user1-5.yaml 2> user1-5.log & 
sleep 162.35; kubectl --namespace="user1" create -f user1-6.yaml 2> user1-6.log & 
kubectl --namespace="user1" create -f user1-7.yaml 2> user1-7.log & 
sleep 162.35; kubectl --namespace="user1" create -f user1-8.yaml 2> user1-8.log & 
kubectl --namespace="user1" create -f user1-9.yaml 2> user1-9.log & 
wait