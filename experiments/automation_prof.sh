rm -rf automation_prof
mkdir automation_prof
python automation_tool.py --test=False --folder=automation_prof --profiling=False --measure=True --measuresec=True --interval=1 --nusers=3 --workload=traces/profiling > automation_prof/automation_tool.log 2>&1 & 
# python get_user_info_timer.py --interval=1 --stopTime=36000 --folder=automation_prof > automation_prof/get_user_info_timer.log 2>&1