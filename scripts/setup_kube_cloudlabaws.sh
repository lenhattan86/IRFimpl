#!/bin/bash
# usage:
# ./kubernetes_cluster.sh masterIP [username] [key file location]
# this script has to be executed on the master node on Chameleon.
# copy the pem/key file to the master node before running this script.
# also manually add hostname to /etc/hosts
#for server in $serverList; do
#		$SSH_CMD $username@$server "sudo sed -i -e 's/127.0.0.1 localhost/127.0.0.1 localhost \n127.0.0.1 $HOSTNAME/g' /etc/hosts" &
#done	
#wait

# cp ~/.ssh/config.chameleon ~/.ssh/config;  005b93.59de673135d75968

# kubeadm join 128.104.222.165:6443 --token z6kryk.l5tbb0xoy9gqcwas --discovery-token-ca-cert-hash sha256:fb55d685d9b96fc86393ce1c0b6003d14831eb698272f3e91de85489f711f437
# remember the git user/pass
# cd..; git config credential.helper store; cd scripts


############# SMALLL ###################
# masterIP="128.110.154.191" #singcpu1
# slavesIP="hp112.utah.cloudlab.us
# " 
# servers="$masterIP
# $slavesIP"
# slavesAWS="52.14.191.65
# 52.14.191.65
# "

# last one of ctl of slave1
# masterIP="128.110.154.154" #singcpu2
# slavesIP="hp080
# " # last one of ctl of slave1
# use old version of OpenStack "before Puke"
LARGE1=true
isPasswordLess=false
isKubernetesCloudlab=false
isKubernetesAWS=true
kubeVersion="1.11.3-00"
# kubeVersion=""
if $isKubernetesAWS
then
	echo "set Kubernetes on AWS"
fi

############### LARGE 1 #################
if $LARGE1
then
	echo "======  large1 ======"
	sleep 5
	masterIP="128.110.154.129"
	slavesIP="hp090.utah.cloudlab.us
hp096.utah.cloudlab.us
hp058.utah.cloudlab.us
hp084.utah.cloudlab.us
hp098.utah.cloudlab.us
hp095.utah.cloudlab.us
hp049.utah.cloudlab.us
hp061.utah.cloudlab.us"

	slavesAWS="3.16.43.102
18.218.248.248
18.223.99.98
18.222.233.82"
else
	echo "======  kube ======"
	sleep 5
	masterIP="128.110.155.10"
	# slavesIP=""

	slavesIP="hp175.utah.cloudlab.us
hp167.utah.cloudlab.us
hp183.utah.cloudlab.us
hp184.utah.cloudlab.us
hp180.utah.cloudlab.us
hp192.utah.cloudlab.us
hp162.utah.cloudlab.us
hp164.utah.cloudlab.us
" 
	slavesAWS=""
fi
############################################# 
username="tanle"
SSH_CMD="ssh "

username_aws="ubuntu"
SSH_CMD_aws="ssh -i tanlesbuaws.pem "

if $isPasswordLess
then
	for server in $servers; do
		scp ~/.ssh/id_rsa* $username@$server:~/.ssh/
		ssh $server "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys ;
			chmod 0600 ~/.ssh/id_rsa*; 
			chmod 0600 ~/.ssh/authorized_keys; 
			rm -rf ~/.ssh/known_hosts; 	
			echo 'StrictHostKeyChecking no' >> ~/.ssh/config"
	done
fi

# #chmod 600 $keyfile
$SSH_CMD $username@$masterIP "echo hello $masterIP" -y
for server in $slavesIP; do
	$SSH_CMD $username@$server "echo hello $server" -y
done
for server in $slavesAWS; do
	$SSH_CMD_aws $username_aws@$server "echo hello $server" -y
done	
echo "Please stop here if one of the node is not connected...."
sleep 15
# setup kubernetes

if $isKubernetesCloudlab
then
	echo "install Kubernetes on CC"
	$SSH_CMD $username@$masterIP 'bash -s' < ./setupkubernetes_cpu.sh $kubeVersion &

	for server in $slavesIP; do
		$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_cpu.sh $kubeVersion &
	done
	wait
fi

if $isKubernetesAWS	
then
	echo "install Kubernetes on AWS"
	for server in $slavesAWS; do
		$SSH_CMD_aws $username_aws@$server 'bash -s' < ./setupkubernetes_gpu.sh $kubeVersion  &
	done
	wait
fi

# configure kubernetes master
$SSH_CMD $username@$masterIP 'bash -s' < ./masterkubeup.sh $masterIP
# c91d8c.c90c8bb2666e5eab  sha256:f3f3d8a49a371628f7086f29d78601bc8e0ff1c2ab48f5a8ffc9696520dd2102

echo "Enter token:"
read token
echo "Enter sha256:"
read sha256
# echo $token > token.txt # save command for using later
# echo $sha256 > sha256.txt
for server in $slavesIP; do
	$SSH_CMD $username@$server 'bash -s' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
for server in $slavesAWS; do
	$SSH_CMD_aws $username_aws@$server 'bash -s' < ./slavejoin.sh $token $sha256 $masterIP &
done
wait
#git config credential.helper store
#https://kukulinski.com/10-most-common-reasons-kubernetes-deployments-fail-part-1/

## install gpu plugin
#kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.9/nvidia-device-plugin.yml
$SSH_CMD $username@$masterIP "kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v1.11/nvidia-device-plugin.yml"