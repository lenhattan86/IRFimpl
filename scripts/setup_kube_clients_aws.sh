#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command

#kubeadm join 128.104.222.154:6443 --token zl1pjj.xrrkncz0leqqwvit --discovery-token-ca-cert-hash sha256:8d7329f797b4045a7eda11fcf6087317b95328f449854df6d641940d8793f353
if [ -z "$1" ]
then
	token="zl1pjj.xrrkncz0leqqwvit"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:8d7329f797b4045a7eda11fcf6087317b95328f449854df6d641940d8793f353"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	masterIP="128.104.222.154"
else
	masterIP="$3"
fi



slavesIP="18.220.84.115
"

username="ubuntu"
SSH_CMD="ssh -i tanlesbuaws.pem "

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