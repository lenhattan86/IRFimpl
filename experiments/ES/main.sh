kubectl delete pod --all --namespace user1
kubectl delete pod --all --namespace user2
sleep 10 
kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
python ../get_user_info.py --user user1 --interval=1 --stopTime=300 --file=user1.csv & 
python ../get_user_info.py --user user2 --interval=1 --stopTime=300 --file=user2.csv & 
./user1.sh &
./user2.sh &
wait