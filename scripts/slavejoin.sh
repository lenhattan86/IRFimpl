#!/bin/bash
#Usage: ./slavejoin.sh [token] [sha256] [masterIPaddress]
#Assumes Kubernetes is already-installed using setupkubernetes.sh

if [ -z "$1" ]
then
	echo "e.g. sudo kubeadm join --token c91d8c.c90c8bb2666e5eab 10.52.1.213:6443 --discovery-token-ca-cert-hash sha256:bda98d8e38201b1328e8039c677572a4b3e33d5843f95626e3cda4028db5d4e8"
else
	token="$1"
fi

if [ -z "$2" ]
then
	echo "sha256"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	echo "Master IP address needed to join worker node to master"
else
	masterIPaddress="$3"
fi

sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl enable kubelet
sudo systemctl start kubelet
for file in /etc/systemd/system/kubelet.service.d/*-kubeadm.conf
do
    echo "Found ${file}"
    FILE_NAME=$file
done
echo "Chosen ${FILE_NAME} as kubeadm.conf"
sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates="Accelerators=true" /g" $FILE_NAME
sudo systemctl daemon-reload
sudo systemctl restart kubelet

sudo kubeadm reset
sudo kubeadm join --token $token $masterIPaddress:6443 --discovery-token-ca-cert-hash $sha256

# support for NodeAffinity
#NVIDIA_GPU_NAME=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader --id=0)
#source /etc/default/kubelet
#KUBELET_OPTS="$KUBELET_OPTS --node-labels='alpha.kubernetes.io/nvidia-gpu-name=$NVIDIA_GPU_NAME'"
#echo "KUBELET_OPTS=$KUBELET_OPTS"
#echo "KUBELET_OPTS=$KUBELET_OPTS" > /etc/default/kubelet
#KUBELET_OPTS=--node-labels='alpha.kubernetes.io/nvidia-gpu-name=Tesla M40'
sudo systemctl daemon-reload
sudo systemctl restart kubelet