kubectl delete pods --all --namespace=default 
echo wait... 
sleep 90 
sudo docker pull lenhattan86/cpu 
sudo docker pull lenhattan86/gpu 
python ../../get_user_info_timer.py --user=default --interval=1 --stopTime=10000 --file=alexnet.csv & pythonScript=$! 
./alexnet-cpu.sh & cpuScript=$! 
./alexnet-gpu.sh & gpuScript=$!
wait