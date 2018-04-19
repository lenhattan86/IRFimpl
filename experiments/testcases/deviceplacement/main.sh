sudo docker pull lenhattan86/ira:cpu 
sudo docker pull lenhattan86/ira:gpu 
kubectl delete pod --all
kubectl delete pod --all --namespace user1
kubectl delete pod --all --namespace user2
kubectl create -f user1.yaml 
python ../get_user_info_timer.py  --interval=1 --stopTime=5250 --file=pods.csv & 
./user1.sh
wait