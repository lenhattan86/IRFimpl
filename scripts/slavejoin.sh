#!/bin/bash
#Usage: ./slavejoin.sh [token] [sha256] [masterIPaddress]
#Assumes Kubernetes is already-installed using setupkubernetes.sh
# kubeadm token create --print-join-command

if [ -z "$1" ]
then
	token="wpifoy.a90o23w2usq5aqor"
else
	token="$1"
fi

if [ -z "$2" ]
then
	sha256="sha256:c5d769d74d407c6500e39e9f2e8c206cedb7f304121f9cb779644accf72a4c4f"
else
	sha256="$2"
fi

if [ -z "$3" ]
then
	masterIPaddress="128.104.222.165"
else
	masterIPaddress="$3"
fi

# sudo iptables -F; sudo swapoff -a ;sudo free -m

sudo docker rmi lenhattan86/bench
sudo docker rmi lenhattan86/ira:cpu
sudo docker rmi lenhattan86/ira:gpu

sudo docker pull lenhattan86/bench
sudo docker pull lenhattan86/ira:cpu
sudo docker pull lenhattan86/ira:gpu

sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl enable kubelet
sudo systemctl start kubelet

# for file in /etc/systemd/system/kubelet.service.d/*-kubeadm.conf
# do
#     echo "Found ${file}"
#     FILE_NAME=$file
# done
# echo "Chosen ${FILE_NAME} as kubeadm.conf"
#sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates="Accelerators=true" /g" $FILE_NAME
# sudo systemctl daemon-reload
# sudo systemctl restart kubelet

sudo kubeadm reset -f
sudo kubeadm join --token $token $masterIPaddress:6443 --discovery-token-ca-cert-hash $sha256

# support for NodeAffinity
#NVIDIA_GPU_NAME=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader --id=0)
#source /etc/default/kubelet
#KUBELET_OPTS="$KUBELET_OPTS --node-labels='alpha.kubernetes.io/nvidia-gpu-name=$NVIDIA_GPU_NAME'"
#echo "KUBELET_OPTS=$KUBELET_OPTS"
#echo "KUBELET_OPTS=$KUBELET_OPTS" > /etc/default/kubelet
#KUBELET_OPTS=--node-labels='alpha.kubernetes.io/nvidia-gpu-name=Tesla M40'
# sudo systemctl daemon-reload
# sudo systemctl restart kubelet