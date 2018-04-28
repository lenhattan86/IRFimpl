#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command

if [ -z "$1" ]
then
	token="f6cyge.vggo875dywsy9931"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:f3b68e827933cdd6c348d40386b391344459c6e78dd1617828ba64ff410a1137"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	masterIP="128.104.222.165"
else
	masterIP="$3"
fi



# slavesIP="18.188.165.51
# 52.15.227.77
# "
slavesIP="18.216.182.131
"

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