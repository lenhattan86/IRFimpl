#!/bin/bash
if [ -z "$1" ]
then
  numberOfCoresStart=1
else
  numberOfCoresStart=$1
fi
if [ -z "$2" ]
then
  numberOfCoreEnd=3
else
  numberOfCoreEnd=$2
fi
for i in $(seq $numberOfCoresStart $numberOfCoreEnd);
do  
  echo $i
done
