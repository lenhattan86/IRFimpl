kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
sleep 30 
user1.sh &
user2.sh &
wait