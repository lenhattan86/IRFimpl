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

# kubeadm join 128.110.153.179:6443 --token brorb7.s0t9ks4k2ikicrtb --discovery-token-ca-cert-hash sha256:f0634ab43ee64189d78db722e88868ce610dfb448725690b38f4f8fd1d84a4a3
# remember the git user/pass
# cd..; git config credential.helper store; cd scripts

echo "This file need to be executed on the master node instead of your local machine for chameleon"
echo "You also need to provide the chameleon.pem file"

masterIP="128.104.222.165"
slavesIP="c220g2-011308.wisc.cloudlab.us		
c220g2-011316.wisc.cloudlab.us		
c220g2-011330.wisc.cloudlab.us		
c220g2-011310.wisc.cloudlab.us		
c220g2-011303.wisc.cloudlab.us		
c220g2-011317.wisc.cloudlab.us		
c220g2-011322.wisc.cloudlab.us		
c220g2-011319.wisc.cloudlab.us		
c220g2-011105.wisc.cloudlab.us		
c220g2-011110.wisc.cloudlab.us		
c220g2-011314.wisc.cloudlab.us		
c220g2-011018.wisc.cloudlab.us
c220g2-011129.wisc.cloudlab.us		
c220g2-011324.wisc.cloudlab.us		
c220g2-011332.wisc.cloudlab.us		
c220g2-031132.wisc.cloudlab.us		
c220g2-011122.wisc.cloudlab.us		
c220g2-011021.wisc.cloudlab.us" # last one of ctl of slave1

serversIP="$masterIP $slavesIP"

username="tanle"
SSH_CMD="ssh "

chmod 600 $keyfile

echo "please enter yes to connect to slaves"
for server in $slavesIP; do
		$SSH_CMD $username@$server "echo hello $server" -y
done	
echo "Please stop here if one of the node is not connected...."
sleep 30
# setup kubernetes
./setupkubernetes_cpu.sh &
for server in $slavesIP; do
	$SSH_CMD $username@$server 'bash -s' < ./setupkubernetes_cpu.sh &
done	
wait

# configure kubernetes master
#$SSH_CMD $username@$master 'bash -s' < ./masterkubeup.sh $masterIP

sudo sh -c "echo '127.0.0.1 $master' >> /etc/hosts"
./masterkubeup.sh $masterIP
#kubeadm join --token c91d8c.c90c8bb2666e5eab 10.52.1.213:6443 --discovery-token-ca-cert-hash sha256:f3f3d8a49a371628f7086f29d78601bc8e0ff1c2ab48f5a8ffc9696520dd2102
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