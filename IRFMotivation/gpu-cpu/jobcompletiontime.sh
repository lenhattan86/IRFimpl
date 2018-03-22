#!/bin/bash
podnames="a100 a50 a10 a5";
kubectl delete pods --all
for name in $podnames; do
	kubectl create -f $name.yaml
	sleep 150
	kubectl logs $name >> log.txt
	echo -e "\n" >> log.txt
done
