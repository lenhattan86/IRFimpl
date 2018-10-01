rm -rf automation_tool
mkdir automation_tool
python automation_tool.py --test False --folder=automation_tool --profiling=True --measure=False --interval=1 --nusers=4 --workload=traces/large > automation_tool/automation_tool.log 2>&1 & 
sleep 120
python get_user_info_timer.py --interval=5 --stopTime=36000 --folder=automation_tool > automation_tool/get_user_info_timer.log 2>&1