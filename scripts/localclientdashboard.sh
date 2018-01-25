#!/bin/bash
#usage: ./localclientsetup.sh [username] [masterIPaddress] [keyfilelocation]
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
ssh-keygen -R $hostIP
#brew install kubectl
mkdir -p  ~/.kube
scp -i $keyfile $hostname@$hostIP:~/config/admin.conf ~/.kube/admin.conf
export KUBECONFIG=~/.kube/admin.conf
kubectl create -f https://git.io/kube-dashboard
echo "######################### Dashboard is now installed, you can run \$kubectl proxy to view the Dashboard ##########################################"
