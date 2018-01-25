#!/bin/bash
# usage:
# ./kubernetes_cluster.sh [username] [key file location]
# this script has to be executed on the master node on Chameleon.
# copy the pem/key file to the master node before running this script.
# also manually add hostname to /etc/hosts
#for server in $serverList; do
#		$SSH_CMD $username@$server "sudo sed -i -e 's/127.0.0.1 localhost/127.0.0.1 localhost \n127.0.0.1 $HOSTNAME/g' /etc/hosts" &
#done	
#wait

master="p100gpus-1";
masterIP="10.40.1.5";
slaves="p100gpus-2 p100gpus-3 p100gpus-4 p100gpus-5 p100gpus-6 p100gpus-7 p100gpus-8 p100gpus-9 p100gpus-10 p100gpus-11 p100gpus-12 p100gpus-13 p100gpus-14 p100gpus-15";
slavesIP="10.40.1.48 10.40.1.49 10.40.1.56 10.40.1.55 10.40.1.54 10.40.1.57 10.40.1.58 10.40.1.65 10.40.1.60 10.40.1.61 10.40.1.62 10.40.1.67 10.40.1.64 10.40.1.68 10.40.1.72";
servers="$master $slaves";
serversIP="$masterIP $slavesIP";

if [ -z "$1" ]56.4
then
	username="cc"
else
	username="$1"
fi
if [ -z "$2" ]
then
	keyfile=~/chameleon.pem
else
	keyfile="$2"
fi
if [ -z "$3" ]
then
	masterIP="10.40.1.5"
else
	masterIP="$3"
fi

#SSH_CMD="ssh -i $keyfile -o \"StrictHostKeyChecking no\" "
SSH_CMD="ssh -i $keyfile "

#./install_tensorflow.sh &
for server in $slavesIP; do
  echo "===== install tensorflow on $server ====="
#  echo $SSH_CMD $server
#  $SSH_CMD $username@$server
#  $SSH_CMD $username@$server 'bash -s' < ./install_tensorflow.sh &
#  ssh -i $keyfile -o "StrictHostKeyChecking no" $username@$server 'bash -s' < ./install_tensorflow.sh &
  ssh -i $keyfile -o "StrictHostKeyChecking no" $username@$server "rm -rf ~/*; git clone https://github.com/lenhattan86/IRFMotivation; git clone https://github.com/lenhattan86/tf_bench "
done	
wait
