kubectl delete pods --all --namespace=defaultsudo docker pull lenhattan86/cpu 
sudo docker pull lenhattan86/gpu 
python ../../get_user_info.py --user=default --interval=1 --stopTime=10000 --file=alexnet.csv & pythonScript=$! 
./alexnet-cpu.sh & cpuScript=$! 
./alexnet-gpu.sh & gpuScript=$!
wait