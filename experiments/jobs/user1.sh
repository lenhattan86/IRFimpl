kubectl create -f user1.yaml 
sleep 30 
kubectl --namespace="user1" create -f user1-0.yaml 2> user1-0.log & 
sleep 1; kubectl --namespace="user1" create -f user1-1.yaml 2> user1-1.log & 
sleep 1; kubectl --namespace="user1" create -f user1-2.yaml 2> user1-2.log & 
sleep 1; kubectl --namespace="user1" create -f user1-3.yaml 2> user1-3.log & 
sleep 1; kubectl --namespace="user1" create -f user1-4.yaml 2> user1-4.log & 
sleep 1; kubectl --namespace="user1" create -f user1-5.yaml 2> user1-5.log & 
sleep 1; kubectl --namespace="user1" create -f user1-6.yaml 2> user1-6.log & 
sleep 1; kubectl --namespace="user1" create -f user1-7.yaml 2> user1-7.log & 
sleep 1; kubectl --namespace="user1" create -f user1-8.yaml 2> user1-8.log & 
sleep 1; kubectl --namespace="user1" create -f user1-9.yaml 2> user1-9.log & 
sleep 1; kubectl --namespace="user1" create -f user1-10.yaml 2> user1-10.log & 
sleep 1; kubectl --namespace="user1" create -f user1-11.yaml 2> user1-11.log & 
sleep 1; kubectl --namespace="user1" create -f user1-12.yaml 2> user1-12.log & 
sleep 1; kubectl --namespace="user1" create -f user1-13.yaml 2> user1-13.log & 
sleep 1; kubectl --namespace="user1" create -f user1-14.yaml 2> user1-14.log & 
sleep 1; kubectl --namespace="user1" create -f user1-15.yaml 2> user1-15.log & 
sleep 1; kubectl --namespace="user1" create -f user1-16.yaml 2> user1-16.log & 
sleep 1; kubectl --namespace="user1" create -f user1-17.yaml 2> user1-17.log & 
sleep 1; kubectl --namespace="user1" create -f user1-18.yaml 2> user1-18.log & 
sleep 1; kubectl --namespace="user1" create -f user1-19.yaml 2> user1-19.log & 
wait