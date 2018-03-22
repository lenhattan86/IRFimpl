#!/usr/bin/env bash

ACTIVATE_TENSORFLOW="source /home/tanle/tensorflow/bin/activate"

num_runs=10

if [ -z "$1" ]
then
  script_1="../benchmarks/linear_regression.py"
#  script_1="../benchmarks/linear_regression_trace.py"
else
  script_1=$1
fi

if [ -z "$2" ]
then
  script_2="../benchmarks/linear_regression_cpu.py"
#  script_2="../benchmarks/linear_regression_cpu_trace.py"
else
  script_2=$2
fi

source /home/tanle/tensorflow/bin/activate
>&2 echo "Running $num_parrallel applications in parallel..."  

for i in `seq 1 $num_runs`;
do
    script=$script_1
    >&2 echo "Starting application $script"
    FULL_COMMAND="python $script"
    (TIMEFORMAT='%R'; time $FULL_COMMAND 2>1.log) 2> 1$i.time &

    script=$script_2
    >&2 echo "Starting application $script_2"
    FULL_COMMAND="python $script_2"
    (TIMEFORMAT='%R'; time $FULL_COMMAND 2>2.log) 2> 2$i.time &
    wait
done

cat *.time > 2_runs_times.csv
rm *.time
