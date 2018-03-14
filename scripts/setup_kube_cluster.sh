#!/bin/bash
# usage:
# ./kubernetes_cluster.sh [username] [key file location]
# this script has to be executed on the master node on Chameleon.
# copy the pem/key file to the master node before running this script.
# also manually add hostname to /etc/hosts
#for server in $serverList; do
#		$SSH_CMD $username@$server "sudo sed -i -e 's/127.0.0.1 localhost/127.0.0.1 localhost \n127.0.0.1 $HOSTNAME/g' /etc/hosts" &
#done	
#wait

#cp ~/.ssh/config.chameleon ~/.ssh/config;  005b93.59de673135d75968

# remember the git user/pass
cd..; git config credential.helper store; cd scripts

echo "This file need to be executed on the master node instead of your local machine for chameleon"
echo "You also need to provide the chameleon.pem file"

masterIP="10.52.1.213";
slavesIP="10.52.1.233"
serversIP="$masterIP $slavesIP";

if [ -z "$1" ]
then
	username="cc"
else
	username="$1"
fi
if [ -z "$2" ]
then
	keyfile=chameleon.pem
else
	keyfile="$2"
fi
if [ -z "$3" ]
then
	echo "no input for master IP"
else
	masterIP="$3"
fi

SSH_CMD="ssh -i $keyfile"

chmod 600 $keyfile

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server "echo hello $slavesIP" -y
done	

# setup kubernetes
./setupkubernetes.sh &
for server in $slavesIP; do
		$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes.sh &
done	
wait

# configure kubernetes master
#$SSH_CMD $username@$master 'bash -s' < ./masterkubeup.sh $masterIP

sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
./masterkubeup.sh $masterIP
#  kubeadm join --token c91d8c.c90c8bb2666e5eab 10.52.1.213:6443 --discovery-token-ca-cert-hash sha256:bda98d8e38201b1328e8039c677572a4b3e33d5843f95626e3cda4028db5d4e8:
echo "Enter command"
read command
for server in $slavesIP; do
		$SSH_CMD $username@$server 'bash -s' < ./slavejoin.sh $command $masterIP &
done
wait

# https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/

