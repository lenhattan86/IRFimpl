kubectl delete pods --all --namespace=default 
echo wait... 
sleep 60 
sudo docker pull lenhattan86/gpu 
sudo docker pull lenhattan86/cpu 
./beta_mov.sh & cpuScript=$! 
python ../get_user_info_timer.py  --interval=1 --stopTime=-1 --file=pods.csv 
