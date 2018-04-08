#!/bin/bash
kubectl create -f ./namespaces/user1.yaml

mkdir logs
mkdir time

defaultJob=alexnet-cpu

./job.sh user1 user1-1 alexnet-cpu 2 0 2

echo "wait..."
sleep 5

kubectl get pods --all-namespaces 

echo "wait..."

sleep 20

kubectl logs --namespace="user1" user1-1

kubectl --namespace="user1" delete pods user1-1