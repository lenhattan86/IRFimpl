#!/usr/bin/env bash

ACTIVATE_TENSORFLOW="source /home/tanle/tensorflow/bin/activate"

num_parrallel=2

if [ -z "$1" ]
then
  script_1="../benchmarks/linear_regression.py"
else
  script_1=$1
fi

if [ -z "$2" ]
then
  script_2="../benchmarks/linear_regression.py"
else
  script_2=$2
fi

source /home/tanle/tensorflow/bin/activate
>&2 echo "Running $num_parrallel applications in parallel..."  

>&2 echo "Starting application $script_1."
FULL_COMMAND="python $script_1"
(TIMEFORMAT='%R'; time $FULL_COMMAND 2>1.log) 2> 1.time &

>&2 echo "Starting application $script_2."
FULL_COMMAND="python $script_2"
(TIMEFORMAT='%R'; time $FULL_COMMAND 2>2.log) 2> 2.time &

wait

cat *.time > times$i.txt
rm *.time
#rm *.log
