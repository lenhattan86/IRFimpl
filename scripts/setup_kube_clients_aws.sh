#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command
 
#kubeadm join 128.110.154.191:6443 --token b5jebd.21z2c0sc3enu904b --discovery-token-ca-cert-hash sha256:80142cbe589638f31c31393f3e897436440e584504c60021026326162911c644
if [ -z "$1" ]
then
	token="b5jebd.21z2c0sc3enu904b"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:80142cbe589638f31c31393f3e897436440e584504c60021026326162911c644"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	# masterIP="128.104.222.154" # 4 cloudlab nodes
	masterIP="128.110.154.191" # 2 cloudlab nodes
else
	masterIP="$3"
fi



# slavesIP="18.222.200.149
# 18.191.216.238
# "

# slavesIP="18.223.164.117
# 18.191.185.180
# "
slavesIP="52.14.191.65
18.221.107.190
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