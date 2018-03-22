#!/bin/bash
## update the system
sudo apt-get update

## common setup
USER="tanle"

## CUDA
# Verify CUDA support
# lspci | grep -i nvidia
# uname -m && cat /etc/*release
sudo apt-get install libcupti-dev
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
sudo apt-get install cuda 
sudo apt install nvidia-profiler
#cuDNN
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170427/cudnn-8.0-linux-x64-v6.0-tgz
tar xvf cudnn-8.0-linux-x64-v6.0.tgz
sudo cp cuda/include/* /usr/local/include
sudo cp cuda/lib64/* /usr/local/cuda/lib64
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170427/Ubuntu16_04_x64/libcudnn6_6.0.21-1+cuda8.0_amd64-deb
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170427/Ubuntu16_04_x64/libcudnn6-dev_6.0.21-1+cuda8.0_amd64-deb
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v6/prod/8.0_20170427/Ubuntu16_04_x64/libcudnn6-doc_6.0.21-1+cuda8.0_amd64
sudo dpkg -i libcudnn6_6.0.21-1+cuda8.0_amd64.deb
sudo dpkg -i libcudnn6-dev_6.0.21-1+cuda8.0_amd64.deb
sudo dpkg -i libcudnn6-doc_6.0.21-1+cuda8.0_amd64.deb

# python libs
sudo pip install matplotlib
sudo apt-get install python-tk

## Tensorflow
virtualenv --system-site-packages ~/tensorflow
source ~/tensorflow/bin/activate
source ~/tensorflow/bin/activate.csh
pip install --upgrade tensorflow-gpu
TF_PYTHON_URL="https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.1.0-cp27-none-linux_x86_64.whl"
sudo pip install --upgrade $TF_PYTHON_URL
source ~/tensorflow/bin/activate
source ~/tensorflow/bin/activate.csh
sudo pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/protobuf-3.1.0-cp27-none-linux_x86_64.whl
echo export LD_LIBRARY_PATH=/usr/local/cuda/lib64/ >> ~/.bashrc
echo export LD_LIBRARY_PATH=/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH >> ~/.bashrc
cd /usr/local/cuda/lib64/; sudo ln -s libcudnn.so.6.* libcudnn.so.5
cd /usr/local/cuda/lib64/; sudo ln -s libcudnn.so.6.* libcudnn.so.5


## Docker
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce

## NVIDIA Docker
# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb

# create a Linux group called docker
sudo groupadd docker
sudo usermod -aG docker $USER
## log out & log in

# Test nvidia-smi
# sudo nvidia-docker run --rm nvidia/cuda nvidia-smi
# sudo nvidia-docker run -it gcr.io/tensorflow/tensorflow:latest-gpu bash

echo "[INFO] Finished installation at: $(date)"

return;

## validate
source ~/tensorflow/bin/activate
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

## end
