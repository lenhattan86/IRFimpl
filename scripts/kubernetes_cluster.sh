#!/bin/bash
# usage:
# ./kubernetes_cluster.sh [hostname] [hostIP] [key file location]
# Example: ./kubernetes_cluster.sh SETCloud 130.127.133.84 ~/Desktop/cloudlab.pem
## constants
if [ -z "$1" ]
then
	hostname="Chameleon/EC-2"
else
	hostname="$1"
fi
if [ -z "$2" ]
then
	hostIP=129.114.109.80
else
	hostIP="$2"
fi
if [ -z "$3" ]
then
	keyfile=~/chamcloud.key
else
	keyfile="$3"
fi
SSH_CMD="ssh -i $keyfile $hostname@$hostIP"
isSetup=true #first time setup: set to true
if $isSetup
then
	$SSH_CMD 'bash -s' < ./setupkubernetes.sh
	isSetup=false
fi
