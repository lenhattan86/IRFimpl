sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all --namespace user2
kubectl delete pod --all --namespace user1
echo wait.... ; sleep 60 
kubectl create -f user2.yaml 
kubectl create -f user1.yaml 
python ../get_user_info_timer.py  --interval=1 --stopTime=5250 --file=pods.csv & 
./user2.sh &
./user1.sh &
wait