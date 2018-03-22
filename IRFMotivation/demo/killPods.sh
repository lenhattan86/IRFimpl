#!/bin/bash
tempFile="pods.txt"
rm -rf $tempFile

COMPLETED="Completed"
ERROR="Error"
timer=2
# periodic kill the completed pods or error
isTiming=true
noResource="No resources found."

while $isTiming; do  
  kubectl get pods --show-all > $tempFile 
  null="NULL"
  while read line; do
    null=$line
    read -a arr <<< $line      
    podName=${arr[0]}
    podStatus=${arr[2]}    
    if [ "$podStatus" == "$COMPLETED" ] || [ "$podStatus" == "$ERROR" ]
    then
      echo "delete $podName"
      kubectl delete pod $podName
    fi
  done < $tempFile
  
  echo $null
  if [ "$null" == "NULL" ]
  then
    echo "=========== No pods available ========="    
    break
  fi
  sleep $timer
done


