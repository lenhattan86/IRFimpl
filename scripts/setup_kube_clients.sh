#!/bin/bash
# usage:

if [ -z "$1" ]
then
	masterIP="128.110.153.179"
else
	masterIP="$1"
fi

serversIP="localhost "

username="tanle"
SSH_CMD="ssh "

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server "echo hello $slavesIP" -y
done	

for server in $slavesIP; do
	$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_gpu.sh &
done	
wait

sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
echo "Enter token:"
read token
echo "Enter sha256:"
read sha256
echo $token > token.txt # save command for using later
echo $sha256 > sha256.txt
for server in $slavesIP; do
	$SSH_CMD $username@$server 'bash -s' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
#git config credential.helper store
#https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/