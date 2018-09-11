# sudo docker pull lenhattan86/ira:cpu 
# sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all
kubectl delete pod --all --namespace user1 --grace-period=0 --force 
kubectl delete pod --all --namespace user2 --grace-period=0 --force 
kubectl create -f user1.yaml 
kubectl create -f user2.yaml 
python ../../get_user_info_timer.py  --interval=1 --stopTime=200 --file=pods.csv & 
./user1.sh &
./user2.sh &
wait