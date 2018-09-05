# job scchedule: 0, 1 --> 3 --> 2
kubectl --namespace="user2" create -f user2-0.yaml 2> user2-0.log & 
sleep 5
kubectl --namespace="user2" create -f user2-1.yaml 2> user2-1.log & 
sleep 5
kubectl --namespace="user2" create -f user2-2.yaml 2> user2-2.log & 