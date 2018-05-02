#!/bin/bash
#usage: ./localclientsetup.sh [username] [masterIPaddress] [keyfilelocation]
if [ -z "$1" ]
then
	username="tanle"
else
	username="$1"
fi
if [ -z "$2" ]
then
	hostIP=128.104.222.165
else
	hostIP="$2"
fi
# if [ -z "$3" ]
# then
# 	keyfile=~/chamcloud.key
# else
# 	keyfile="$3"
# fi
ssh-keygen -R $hostIP
#brew install kubectl
sudo apt-get purge -y kubelet kubeadm kubectl kubernetes-cni
sudo apt-get install -y kubectl
mkdir -p  ~/.kube
# scp -i $keyfile $username@$hostIP:~/config/admin.conf ~/.kube/admin.conf
scp $username@$hostIP:~/config/admin.conf ~/.kube/admin.conf
export KUBECONFIG=~/.kube/admin.conf
kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
# kubectl create clusterrolebinding --user system:serviceaccount:kube-system:kubernetes-dashboard kube-system-cluster-admin --clusterrole cluster-admin
kubectl create clusterrolebinding root-cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:kube-system:kubernetes-dashboard
echo "######################### Dashboard is now installed, you can run \$kubectl proxy to view the Dashboard ##########################################"
