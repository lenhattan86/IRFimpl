python ../../get_user_info.py --user=default --interval=1 --stopTime=-1 --file=alexnet.csv & 
./alexnet_cpu.sh &
./alexnet_gpu.sh &
wait