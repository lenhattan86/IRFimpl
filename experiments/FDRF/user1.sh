kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
sleep 2582.3; kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
wait