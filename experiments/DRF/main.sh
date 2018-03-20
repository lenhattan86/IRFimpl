kubectl delete pod --all --namespace user1
kubectl delete pod --all --namespace user2
sleep 10 
./user1.sh &
./user2.sh &
wait