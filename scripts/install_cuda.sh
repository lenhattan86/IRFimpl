echo "################################# Install nvidia-375 ######################################"
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:graphics-drivers
sudo apt-get update
sudo apt install -y nvidia-375
echo "######################### CUDA, CuDNN ##########################################"
sudo apt-get install -y linux-headers-$(uname -r)
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
mv cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb  cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb
sudo apt-get update
sudo apt-get install -y cuda
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
wget https://www.dropbox.com/s/vrhgg7z856402s6/cudnn-8.0-linux-x64-v5.1.tgz
tar -xzvf cudnn-8.0-linux-x64-v5.1.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
sudo rm cudnn-8.0-linux-x64-v6.0.tgz
echo "######################### CUPTI-DEV ##########################################"
wget https://www.dropbox.com/s/n683yo6vrb9ip5r/cuptiruntime.deb
wget https://www.dropbox.com/s/g644z0kgcsdvra1/cuptidevlib.deb
wget https://www.dropbox.com/s/uoxd92ecc9dwbmt/cuptidoclib.deb
sudo dpkg -i cuptiruntime.deb
sudo dpkg -i cuptidevlib.deb
sudo dpkg -i cuptidoclib.deb
sudo apt-get update
sudo apt-get install -y libcupti-dev
sudo rm *.deb

# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb
sudo usermod -a -G docker $USER # need to log out and loging
# Test nvidia-smi
#nvidia-docker run --rm nvidia/cuda nvidia-smi
