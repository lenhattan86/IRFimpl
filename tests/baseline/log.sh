#!/bin/bash

if [ -z "$1" ]
then
	echo "./log.sh username podname"
	exit
fi

if [ -z "$2" ]
then
	echo "./log.sh username podname"
	exit
fi

mkdir logs

COMPLETED="Completed"
RUNNING="Running"
Creating="ContainerCreating"
ERROR="Error"
timer=1
# periodic kill the completed pods or error
isTiming=true
noResource="No resources found."

podName=$2
username=$1

tempFile="logs/$podName.tmp"
rm -rf $tempFile

logFile="logs/$podName.log"

start_time="$(date -u +%s.%N)"
# echo "submitted, $(date +%s)" > $logFile
creating_time=0
running_time=0
sleep $timer

isNotCreated=true
isNotRunning=true

while $isTiming; do  
  kubectl get pods $podName --namespace $username > $tempFile 
#  kubectl get pods --all-namespaces
  null="NULL"
  isNothing=true
  while read line; do
    null=$line
    read -a arr <<< $line      
	    podName=${arr[0]}
	    podStatus=${arr[2]}

    if $isNotCreated
    then
		if [ "$podStatus" == "$Creating" ]
	    then
	      echo "$podName creating"
	      #kubectl delete pod $podName
	      creating_time="$(date -u +%s.%N)"
	      # echo "creating, $(date +%s) " >> $logFile
	      isNotCreated=false
	    fi
	fi

	if $isNotRunning	
	then
	    if [ "$podStatus" == "$RUNNING" ]
	    then
	      running_time="$(date -u +%s.%N)"
	      echo "$podName Running"
	      #kubectl delete pod $podName
	      # echo "Running, $(date +%s) " >> $logFile
	    fi
	    isNotRunning=false
	fi

    if [ "$podStatus" == "$COMPLETED" ]
    then
      echo "$podName completed"      
      # echo "completed, $(date +%s)" >> $logFile
      end_time="$(date -u +%s.%N)"
      kubectl delete pod $podName --namespace $username

      elapsed1="$(bc <<<"$end_time-$start_time")"
      elapsed2="$(bc <<<"$end_time-$creating_time")"
      elapsed3="$(bc <<<"$end_time-$running_time")"
      
      echo "$podName, $start_time, $creating_time, $running_time, $end_time, $elapsed1, $elapsed2, $elapsed3, " >> logs/time.log
      exit
    fi

  isNothing=false  
  done < $tempFile
	  
  if $isNothing
  then
  	break;
  fi

  sleep $timer
done