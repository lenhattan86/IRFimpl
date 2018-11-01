#!/bin/bash
#usage: ./setupkubernetes.sh

kubeVer=$1
sudo apt-get purge -y kubelet kubeadm kubectl kubernetes-cni
sudo apt-get purge -y docker-ce

# echo "######################### DOCKER ##########################################"
# sudo apt-get install libltdl7
# sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
# wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
# sudo dpkg -i docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
# #sudo apt install -y docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
# sudo groupadd docker
# sudo usermod -aG docker $USER

## move docker images to another folder
# sudo mkdir /dev/projects; sudo chmod 777 /dev/projects; mkdir /dev/projects/docker
# sudo sed -i -e "s/ExecStart=\/usr\/bin\/dockerd -H /ExecStart=\/usr\/bin\/dockerd -g \/dev\/projects\/docker -H /g" /lib/systemd/system/docker.service
# sudo systemctl stop docker
# sudo systemctl daemon-reload
# sudo rsync -aqxP /var/lib/docker/ /dev/projects/docker
# sudo systemctl start docker
# echo 'You might need to reboot / relogin to make docker work correctly'


echo "##############install docker-ce ###########"
sudo apt-get update 

sudo apt-get install -y \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install -y docker-ce   

echo "######################### KUBERNETES ##########################################"
sudo bash -c 'apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update'
# sudo apt-get install -y kubelet kubeadm kubectl 
if [ -z "$1" ]
then
	sudo apt-get install -y kubelet kubeadm kubectl
else	
    sudo apt-get install -qy kubelet=$1 kubeadm=$1 kubectl=$1
fi
sudo apt-get install -y kubernetes-cni

# sudo apt-get install -qy kubernetes-cni=0.5.0

# disable swap
sudo iptables -F; sudo swapoff -a; sudo free -m

echo "######################### KUBEADM RESET ##########################################"
sudo kubeadm reset -f
# sudo kubeadm reset
echo "######################### Clean-up ##########################################"
sudo rm -rf *.tgz *.deb

echo "######################### DOCKER-PULL ##########################################"
sudo docker rmi lenhattan86/ira:cpu
sudo docker pull lenhattan86/ira:cpu