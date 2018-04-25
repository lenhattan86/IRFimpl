#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command

if [ -z "$1" ]
then
	masterIP="128.104.222.165"
else
	masterIP="$1"
fi

if [ -z "$2" ]
then
	token="lzmo7g.rrp7ewxqs957piny"
else
	token="$2"
fi

if [ -z "$3" ]
then
	sha256="sha256:fb55d685d9b96fc86393ce1c0b6003d14831eb698272f3e91de85489f711f437"
else
	sha256="$3"
fi

# slavesIP="18.188.165.51
# 52.15.227.77
# "
slavesIP="18.216.47.201
18.191.5.171
18.188.243.138
13.58.60.148
18.217.218.220
18.217.58.195
18.217.156.249
18.219.60.52
18.221.243.39
18.191.13.109
18.220.117.165
13.58.212.39"

username="ubuntu"
SSH_CMD="ssh -i tanlesbuaws.pem "

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server " echo hello $server"
done	

# for server in $slavesIP; do
# 	$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_gpu.sh &
# done	

# sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
for server in $slavesIP; do
	$SSH_CMD $username@$server ' bash -s ' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
#git config credential.helper store
#https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/