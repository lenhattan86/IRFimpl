#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command

if [ -z "$1" ]
then
	token="snjxkk.crtlqks7coc7jogo"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:896c1bc82068fb7d8027560cef91f2fa1909311a2fccb248fb7e3a3cd8df4c1f"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	masterIP="128.104.222.123"
else
	masterIP="$3"
fi



slavesIP="129.114.108.226
"

username="cc"
SSH_CMD="ssh -i chameleon.pem "

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server " echo hello $server"
done	

for server in $slavesIP; do
  	$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_gpu.sh &
done	
wait

# sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
for server in $slavesIP; do
	$SSH_CMD $username@$server ' bash -s ' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
#git config credential.helper store
#https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/