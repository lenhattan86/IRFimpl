kubectl create -f user2.yaml 
sleep 0; kubectl --namespace="user2" create -f user2-0.yaml 2> user2-0.log & 
sleep 0; kubectl --namespace="user2" create -f user2-1.yaml 2> user2-1.log & 
sleep 0; kubectl --namespace="user2" create -f user2-2.yaml 2> user2-2.log & 
sleep 0; kubectl --namespace="user2" create -f user2-3.yaml 2> user2-3.log & 
sleep 1; sleep 50; kubectl --namespace="user2" create -f user2-4.yaml 2> user2-4.log & 
sleep 0; kubectl --namespace="user2" create -f user2-5.yaml 2> user2-5.log & 
sleep 0; kubectl --namespace="user2" create -f user2-6.yaml 2> user2-6.log & 
sleep 0; kubectl --namespace="user2" create -f user2-7.yaml 2> user2-7.log & 
sleep 1; sleep 50; kubectl --namespace="user2" create -f user2-8.yaml 2> user2-8.log & 
sleep 0; kubectl --namespace="user2" create -f user2-9.yaml 2> user2-9.log & 
sleep 0; kubectl --namespace="user2" create -f user2-10.yaml 2> user2-10.log & 
sleep 0; kubectl --namespace="user2" create -f user2-11.yaml 2> user2-11.log & 
sleep 1; sleep 50; kubectl --namespace="user2" create -f user2-12.yaml 2> user2-12.log & 
sleep 0; kubectl --namespace="user2" create -f user2-13.yaml 2> user2-13.log & 
sleep 0; kubectl --namespace="user2" create -f user2-14.yaml 2> user2-14.log & 
sleep 0; kubectl --namespace="user2" create -f user2-15.yaml 2> user2-15.log & 
wait