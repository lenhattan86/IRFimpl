kubectl create -f user2.yaml 
sleep 30 
kubectl --namespace="user2" create -f user2-0.yaml 2> user2-0.log & 
kubectl --namespace="user2" create -f user2-1.yaml 2> user2-1.log & 
kubectl --namespace="user2" create -f user2-2.yaml 2> user2-2.log & 
kubectl --namespace="user2" create -f user2-3.yaml 2> user2-3.log & 
sleep 1; kubectl --namespace="user2" create -f user2-4.yaml 2> user2-4.log & 
kubectl --namespace="user2" create -f user2-5.yaml 2> user2-5.log & 
kubectl --namespace="user2" create -f user2-6.yaml 2> user2-6.log & 
kubectl --namespace="user2" create -f user2-7.yaml 2> user2-7.log & 
sleep 1; kubectl --namespace="user2" create -f user2-8.yaml 2> user2-8.log & 
kubectl --namespace="user2" create -f user2-9.yaml 2> user2-9.log & 
kubectl --namespace="user2" create -f user2-10.yaml 2> user2-10.log & 
kubectl --namespace="user2" create -f user2-11.yaml 2> user2-11.log & 
sleep 1; kubectl --namespace="user2" create -f user2-12.yaml 2> user2-12.log & 
kubectl --namespace="user2" create -f user2-13.yaml 2> user2-13.log & 
kubectl --namespace="user2" create -f user2-14.yaml 2> user2-14.log & 
kubectl --namespace="user2" create -f user2-15.yaml 2> user2-15.log & 
wait