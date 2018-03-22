python ../../get_user_info.py --user=default --interval=1 --stopTime=-1 --file=alexnet.csv & 
./alexnet-cpu.sh &
./alexnet-gpu.sh &
wait