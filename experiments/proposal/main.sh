sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pods --all
kubectl delete priorityClasses --all

kubectl create -f priority-140.yaml
kubectl create -f priority-160.yaml
kubectl create -f priority-80.yaml
echo wait.... ; 
sleep 60
./user1.sh &
./user2.sh &
./user3.sh &
./user4.sh &
sleep 0; python ../get_user_info_timer.py  --interval=1 --stopTime=3000 --file=pods.csv 
