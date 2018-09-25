#!/bin/bash
#usage: ./setupkubernetes.sh

kubeVer="1.11.3-00"
sudo apt-get purge -y kubelet kubeadm kubectl kubernetes-cni

echo "################################# Install nvidia-384 ######################################"
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:graphics-drivers -y
sudo apt-get update -y
sudo apt purge -y nvidia*
#sudo apt install -y nvidia-375
sudo apt install -y nvidia-384
echo "######################### CUDA, CuDNN ##########################################"
sudo apt-get purge -y cuda
sudo apt-get install -y linux-headers-$(uname -r)
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
mv cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb  cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb
sudo apt-get update
sudo apt-get install -y cuda # this also incall nvidia-384
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
#wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb
#mv cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64-deb  cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
#sudo dpkg -i cuda-repo-ubuntu1604-9-0-local_9.0.176-1_amd64.deb
#sudo apt-get update
#sudo apt-get install -y cuda # this also incall nvidia-384
#export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}
#export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"

#https://www.dropbox.com/s/zzk1u252b6vj72q/cudnn-8.0-linux-x64-v5.1.tgz
#https://www.dropbox.com/s/e6uhqfwthn6o6x6/cudnn-9.0-linux-x64-v7.1.tgz
wget https://www.dropbox.com/s/ygjvedybap9p577/cudnn-8.0-linux-x64-v5.1.tgz
tar -xzvf cudnn-8.0-linux-x64-v5.1.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
sudo rm cudnn-8.0-linux-x64-v5.1.tgz
echo "==================testing cuda drivers===================="
nvidia-smi
#sudo apt install nvidia-cuda-toolkit
echo "######################### CUPTI-DEV ##########################################"
wget https://www.dropbox.com/s/n683yo6vrb9ip5r/cuptiruntime.deb & 
wget https://www.dropbox.com/s/g644z0kgcsdvra1/cuptidevlib.deb &
wget https://www.dropbox.com/s/uoxd92ecc9dwbmt/cuptidoclib.deb &
wait
sudo dpkg -i cuptiruntime.deb
sudo dpkg -i cuptidevlib.deb
sudo dpkg -i cuptidoclib.deb
sudo apt-get update -y
sudo apt-get install -y libcupti-dev
sudo rm *.deb
echo "######################### DOCKER ##########################################"
# sudo apt-get libltdl7
# sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
# wget https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
# sudo dpkg -i docker-engine_1.12.6-0~ubuntu-xenial_amd64.deb
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

echo "######################### NVIDIA-DOCKER ##########################################"

# docker 1.0
# wget https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
# sudo dpkg -i nvidia-docker_1.0.1-1_amd64.deb
# sudo apt-get install -f -y

##
#wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
#sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb
#sudo apt-get install -f
# install from sources instead.
#git clone https://github.com/NVIDIA/nvidia-docker
#make deb
#cd dist
#sudo dpkg -i nvidia-docker_1.0.1-1_amd64.deb
#sudo apt-get install -f
#rm -rf nvidia-docker
#cd ..
# test nvidia-docker: sudo nvidia-docker-plugin
#apt-get install nvidia-modprobe
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

echo "###################### install nvidia docker 2.0  ###############################"
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge -y nvidia-docker

# Add the package repositories
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi

sudo tee /etc/docker/daemon.json <<EOF
{
    "default-runtime": "nvidia",
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
EOF

sudo pkill -SIGHUP dockerd


echo "######################### KUBERNETES ##########################################"
sudo bash -c 'apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update'
#sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-get install -qy kubelet=$kubeVer kubeadm=$kubeVer kubectl=$kubeVer
sudo apt-get install -y kubernetes-cni

# sudo systemctl restart kubelet

# Verify
#sudo docker run --rm nvidia/cuda nvidia-smi

echo "######################### PATH ##########################################"
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
echo "######################### KUBEADM RESET ##########################################"
sudo kubeadm reset -f
echo "######################### Clean-up ##########################################"
sudo rm -rf *.tgz *.deb

echo "######################### DOCKER-PULL ##########################################"
# sudo docker rmi lenhattan86/bench
sudo docker rmi lenhattan86/ira:cpu
sudo docker rmi lenhattan86/ira:gpu

# sudo docker pull lenhattan86/bench
sudo docker pull lenhattan86/ira:cpu
sudo docker pull lenhattan86/ira:gpu

# tensorflow
#https://pypi.python.org/packages/1b/36/478c5cc40b280061130c30acad118940b442d35b36e11c7ffedd652db58f/tensorflow_gpu-1.1.0-cp27-cp27mu-manylinux1_x86_64.whl#md5=bd1bc90cbd2957947c16b08a4535bc21


