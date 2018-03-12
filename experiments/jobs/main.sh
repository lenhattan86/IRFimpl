kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
kubectl create -f user3.yaml 
sleep 30 
user1.sh &
user2.sh &
user3.sh &
wait