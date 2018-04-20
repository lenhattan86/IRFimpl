kubectl delete pods --all --namespace=default --grace-period=0 --force 
echo wait... 
sleep 60 
sudo docker pull lenhattan86/gpu 
sudo docker pull lenhattan86/cpu 
python ../get_user_info_timer.py  --interval=1 --stopTime=36000 --file=beta_mov.csv & pythonScript=$! 
./beta_mov.sh & cpuScript=$! 
wait