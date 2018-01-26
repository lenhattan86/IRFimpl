#!/bin/bash
sudo apt install bc

mkdir logs
mkdir jobs

rm -rf logs/time.log

userid="user1 user2 user3";
initTime=1

sudo docker pull lenhattan86/bench

isCreatNameSpace=true
if $isCreatNameSpace
then
  for user in $userid; do
	  kubectl create -f ./namespaces/$user.yaml
  done	
fi



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
		./job.sh $userName $userName-$i "$jobName" $cpu $gpu $mem &
		sleep $period
	done
	wait
}

START=$(date +%s)

user_func user1 3 1 3 2 "sleep 30" 30 &
sleep 15
user_func user2 3 26 1 2 "sleep 30" 30 & 
user_func user3 3 26 0 2 "sleep 30" 30 & 

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"
echo "It took $DIFF seconds" > runner.logs
# kubectl get pods --all-namespaces --show-all