#!/bin/bash
tempFile="podsDeleted.txt"
rm -rf $tempFile

kubectl delete pods --all > $tempFile

timer=2
# periodic kill the completed pods or error
isTiming=true

while $isTiming; do  
  kubectl get pods --show-all > $tempFile
  null="NULL"
  while read line; do
    null=$line    
  done < $tempFile
  
  if [ "$null" == "NULL" ]
  then
    echo "=========== All pods are deleted ========="    
    isTiming=false
    break
  fi
  sleep $timer
done


