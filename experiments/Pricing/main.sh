sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all --namespace user1
kubectl delete pod --all --namespace user2
kubectl delete pod --all --namespace user3
kubectl delete pod --all --namespace user4
echo wait.... ; sleep 60 
kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
kubectl create -f user3.yaml 
kubectl create -f user4.yaml 
./user1.sh &
./user2.sh &
./user3.sh &
./user4.sh &
sleep 0; python ../get_user_info_timer.py  --interval=1 --stopTime=10800 --file=pods.csv 
