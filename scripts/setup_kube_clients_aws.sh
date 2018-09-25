#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command

#kubeadm join 128.104.222.154:6443 --token f5wkdp.so57sxcurzacf9fs --discovery-token-ca-cert-hash sha256:87e8674de5aa719b2b03c0fe545e36f38bd253ad0ac628f0678f24156493459f
if [ -z "$1" ]
then
	token="x7u62c.ketr1rlg95zhjlnk"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:87e8674de5aa719b2b03c0fe545e36f38bd253ad0ac628f0678f24156493459f"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	masterIP="128.104.222.154"
else
	masterIP="$3"
fi



slavesIP="18.220.20.132
"

username="ubuntu"
SSH_CMD="ssh -i tanlesbuaws.pem "

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server " echo hello $server"
done	

# for server in $slavesIP; do
#   	$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_gpu.sh &
# done	
# wait

# sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
for server in $slavesIP; do
	$SSH_CMD $username@$server ' bash -s ' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
#git config credential.helper store
#https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/