sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all

kubectl create -f priority-40.yaml
kubectl create -f priority-60.yaml
kubectl create -f priority-120.yaml
echo wait.... ; 
sleep 10
./user1.sh &
./user2.sh &
./user3.sh &
./user4.sh &
sleep 0; python ../get_user_info_timer.py  --interval=1 --stopTime=1000 --file=pods.csv 
