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

echo "submitted, $(date +%s)" > $logFile

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
	      echo "creating, $(date +%s) " >> $logFile
	      isNotCreated=false
	    fi
	fi

	if $isNotRunning	
	then
	    if [ "$podStatus" == "$RUNNING" ]
	    then
	      echo "$podName Running"
	      #kubectl delete pod $podName
	      echo "Running, $(date +%s) " >> $logFile
	    fi
	    isNotRunning=false
	fi

    if [ "$podStatus" == "$COMPLETED" ]
    then
      echo "$podName completed"      
      echo "completed, $(date +%s)" >> $logFile
      kubectl delete pod $podName --namespace $username
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