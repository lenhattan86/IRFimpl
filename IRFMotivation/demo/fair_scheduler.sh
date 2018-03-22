#!/bin/bash
userid="user1 user2";
initTime=1

isCreatNameSpace=true
if $isCreatNameSpace
then
  for user in $userid; do
	  kubectl create -f ./namespaces/$user.yaml
  done	
fi

mkdir logs
mkdir time

user1_num=4
user1="user1"
user1_func () { 	
	for i in `seq 1 4`;
	do  
		./job.sh $user1 $user1-$i alexnet-cpu 23 0 4 &
	done

	for i in `seq 1 $user1_num`;
	do  	
		for i in `seq 1 4`;
		do  
			./job.sh $user1 $user1-$i alexnet-gpu 1 1 4 &
		done
		sleep 150
	done
}

user2_num=5
user2_func () { 
	for i in `seq 1 $user2_num`;
	do  	
		for i in `seq 1 4`;
		do  
			./job.sh $user2 $user1-$i alexnet-cpu 23 0 4 &
			./job.sh $user2 $user1-$i alexnet-gpu 1 1 4 &
		done
		sleep 115
	done
}

START=$(date +%s)

initTime=20
user1_func &
user2_func &

sleep $initTime
./killPods.sh

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"