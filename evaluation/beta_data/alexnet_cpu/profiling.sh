kubectl delete pods --all --namespace=default 
echo wait... 
sleep 60 
sudo docker pull lenhattan86/gpu 
python ../../get_user_info_timer.py  --interval=1 --stopTime=36000 --file=alexnet.csv & pythonScript=$! 
./alexnet.sh & cpuScript=$! 
wait