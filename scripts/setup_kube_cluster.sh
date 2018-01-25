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

echo "This file need to be executed on the master node instead of your local machine for chameleon"
echo "You also need to provide the chameleon.pem file"

master="gpus";
masterIP="129.114.108.87";
slavesIP=""
slaves=""
servers="$master $slaves";
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
echo "Enter Token :"
read token
for server in $slavesIP; do
		$SSH_CMD $username@$server 'bash -s' < ./slavejoin.sh $token $masterIP &
done
wait

# https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/

