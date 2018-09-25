kubectl delete pods --all --namespace=default  
echo wait... 
sleep 15 
./profiling.sh & 
python ../get_user_info_timer.py  --interval=1 --stopTime=36000 
