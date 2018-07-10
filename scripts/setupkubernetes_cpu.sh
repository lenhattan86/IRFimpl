#!/bin/bash
#usage: ./setupkubernetes.sh

kubeVer="1.9.6-00"
sudo apt-get purge -y kubelet kubeadm kubectl kubernetes-cni

echo "######################### DOCKER ##########################################"
sudo apt-get libltdl7
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
sudo dpkg -i docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
#sudo apt install -y docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
sudo groupadd docker
sudo usermod -aG docker $USER

sudo mkdir /dev/projects; sudo chmod 777 /dev/projects; mkdir /dev/projects/docker
sudo sed -i -e "s/ExecStart=\/usr\/bin\/dockerd -H /ExecStart=\/usr\/bin\/dockerd -g \/dev\/projects\/docker -H /g" /lib/systemd/system/docker.service
sudo systemctl stop docker
sudo systemctl daemon-reload
sudo rsync -aqxP /var/lib/docker/ /dev/projects/docker

sudo systemctl start docker
echo 'You might need to reboot / relogin to make docker work correctly'

echo "######################### KUBERNETES ##########################################"
sudo bash -c 'apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update'
#sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
sudo apt-get install -qy kubelet=$kubeVer kubeadm=$kubeVer kubectl=$kubeVer kubernetes-cni=$kubeVer

sudo iptables -F
sudo swapoff -a
sudo free -m

echo "######################### KUBEADM RESET ##########################################"
sudo kubeadm reset -f
echo "######################### Clean-up ##########################################"
sudo rm -rf *.tgz *.deb

echo "######################### DOCKER-PULL ##########################################"
sudo docker rmi lenhattan86/bench
sudo docker rmi lenhattan86/ira:cpu

sudo docker pull lenhattan86/bench
sudo docker pull lenhattan86/ira:cpu

