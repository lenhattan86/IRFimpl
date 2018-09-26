#!/bin/bash
# usage:

# using the following command to create token on server
# sudo kubeadm token create --print-join-command
 #kubeadm join 128.110.154.154:6443 --token erulu6.5p6rpigef2g3oxou --discovery-token-ca-cert-hash sha256:46638d849c6c93df09b02b199a78327e15b8720de49fa73a7524918ce689de4e


cloudLabServers="hp110.utah.cloudlab.us		
hp112.utah.cloudlab.us
hp073.utah.cloudlab.us
hp080.utah.cloudlab.us
"
awsServers="18.223.164.117
18.191.185.180
52.14.191.65
18.221.107.190
"
# slavesIP="52.14.191.65
# 18.221.107.190
# "
SSH_CMD="ssh -i tanlesbuaws.pem "
for server in $cloudLabServers; do
	SSH_CMD="ssh "
	username="tanle"
	$SSH_CMD $username@$server " echo hello $server" 
done	
for server in $awsServers; do
	SSH_CMD="ssh -i tanlesbuaws.pem "
	username="ubuntu"
	$SSH_CMD $username@$server " echo hello $server" 
done
############## 
for server in $cloudLabServers; do
	SSH_CMD="ssh "
	username="tanle"
	$SSH_CMD $username@$server " sudo docker rmi --force lenhattan86/ira:cpu; sudo docker pull lenhattan86/ira:cpu" &
done	
wait
for server in $awsServers; do
	SSH_CMD="ssh -i tanlesbuaws.pem "
	username="ubuntu"
	# $SSH_CMD $username@$server " sudo docker rmi --force lenhattan86/ira:cpu; sudo docker pull lenhattan86/ira:cpu" &
	$SSH_CMD $username@$server " sudo docker rmi --force lenhattan86/ira:gpu; sudo docker pull lenhattan86/ira:gpu" &
done
wait