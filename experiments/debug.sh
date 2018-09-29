rm -rf debug
mkdir debug
python automation_tool.py --test False --folder=debug --profiling=False --measure=False --interval=1 --nusers=4 --workload=traces/debug > debug/automation_tool.log 2>&1