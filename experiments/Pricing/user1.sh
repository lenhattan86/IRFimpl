sleep 1; kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
sleep 1; kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
sleep 1; kubectl --namespace="user1" create -f user1-2.yaml 2> user1-2.log & 
sleep 162; kubectl --namespace="user1" create -f user1-3.yaml 2> user1-3.log & 
sleep 1; kubectl --namespace="user1" create -f user1-4.yaml 2> user1-4.log & 
sleep 1; kubectl --namespace="user1" create -f user1-5.yaml 2> user1-5.log & 
wait