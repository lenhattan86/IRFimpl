#!/usr/bin/env bash

ACTIVATE_TENSORFLOW="source /home/tanle/tensorflow/bin/activate"

if [ -z "$1" ]
then
  num_parrallel=1
else
  num_parrallel=$1
fi

if [ -z "$2" ]
then
  tf_file="linear_regression.py"
else
  tf_file=$2
fi
source /home/tanle/tensorflow/bin/activate
>&2 echo "Running $num_parrallel applications in parallel..."  
for i in `seq 1 $num_parrallel`;
do
    >&2 echo "Starting application $i."
    FULL_COMMAND="python $tf_file"    
	(TIMEFORMAT='%R'; time $FULL_COMMAND 2>application$i.log) 2> $i.time &
done
wait

cat *.time > times$i.txt
rm *.time
