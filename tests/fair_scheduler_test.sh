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
	for i in `seq 1 $jobNum`;
	do  
		./job.sh $userName $userName-$i $jobName $cpu $gpu $mem &
	done
}

START=$(date +%s)

initTime=20
# Use up full resources for user 1
echo "Use up full resources for user 1"
user_func user1 4 2 0 2 $defaultJob

#sleep $initTime
#./killPods.sh

# Queue up 2 jobs for user 1, 2 jobs for user 2.
echo "Queue up 2 jobs for user 1, 2 jobs for user 2."
user_func user1 2 2 0 2 $defaultJob
sleep 5
user_func user2 2 2 0 2 $defaultJob

# Expected results: 2 jobs of user 2 are served first than 2 jobs of user 1.

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"
# kubectl get pods --all-namespaces --show-all
