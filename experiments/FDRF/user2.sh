sleep 0; kubectl --namespace="user2" create -f user2-0.yaml 2> user2-0.log & 
sleep 0; kubectl --namespace="user2" create -f user2-1.yaml 2> user2-1.log & 
sleep 0; kubectl --namespace="user2" create -f user2-2.yaml 2> user2-2.log & 
sleep 50; kubectl --namespace="user2" create -f user2-3.yaml 2> user2-3.log & 
sleep 50; kubectl --namespace="user2" create -f user2-4.yaml 2> user2-4.log & 
sleep 0; kubectl --namespace="user2" create -f user2-5.yaml 2> user2-5.log & 
sleep 0; kubectl --namespace="user2" create -f user2-6.yaml 2> user2-6.log & 
sleep 50; kubectl --namespace="user2" create -f user2-7.yaml 2> user2-7.log & 
wait