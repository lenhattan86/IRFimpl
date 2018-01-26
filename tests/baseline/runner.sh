#!/bin/bash
userid="user1 user2";
initTime=1

sudo docker pull lenhattan86/bench

isCreatNameSpace=true
if $isCreatNameSpace
then
  for user in $userid; do
	  kubectl create -f ./namespaces/$user.yaml
  done	
fi

mkdir logs
mkdir jobs
mkdir time

defaultJob=alexnet-cpu

user_func () { 	
	# user_func userName jobNum cpu gpu mem jobName
	userName=$1
	jobNum=$2
	cpu=$3
	gpu=$4
	mem=$5
	jobName=$6
	period=$7
	for i in `seq 1 $jobNum`;
	do  
		./job.sh $userName $userName-$i $jobName $cpu $gpu $mem &
		sleep $period
	done
	wait
}

START=$(date +%s)

user_func user1 2 4 0 2 "sleep 5" 5 &
user_func user2 2 1 1 2 "sleep 5" 5

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"
echo "It took $DIFF seconds" > runner.logs
# kubectl get pods --all-namespaces --show-all
