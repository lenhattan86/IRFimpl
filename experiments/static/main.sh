sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all --namespace user1
kubectl delete pod --all --namespace user2
echo wait.... ; sleep 60 
kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
./user1.sh &
./user2.sh &
sleep 0; python ../get_user_info_timer.py  --interval=5 --stopTime=2400 --file=pods.csv 
