echo "######################### install utilities ##########################################"
sudo apt-get install -y sysstat
echo "################################# Install nvidia-375 ######################################"
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:graphics-drivers
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
echo "PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}" >> ~/.bashrc
echo "LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"  " >> ~/.bashrc
# cudnn version 5
wget https://www.dropbox.com/s/vrhgg7z856402s6/cudnn-8.0-linux-x64-v5.1.tgz
tar -xzvf cudnn-8.0-linux-x64-v5.1.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
sudo rm cudnn-8.0-linux-x64-v5.1.tgz
rm -rf cuda
# cudnn version 6
wget https://www.dropbox.com/s/56tkkrs2pqyrauv/libcudnn6_6.0.21-1%2Bcuda8.0_amd64.deb
sudo dpkg -i libcudnn6_6.0.21-1+cuda8.0_amd64.deb
rm libcudnn6_6.0.21-1+cuda8.0_amd64.deb
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

echo "######################### TENSORFLOW PIP ##########################################"
sudo apt-get install -y python-dev python-pip
pip install --upgrade pip
sudo -H pip install -U pip setuptools
sudo pip install tensorflow-gpu
