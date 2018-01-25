#!/bin/bash
#usage: ./masterkubeup.sh [masterIPaddress]
sudo kubeadm reset 
if [ -z "$1" ]
then
	ipaddress="129.114.109.80"
else
	ipaddress="$1"
fi

sudo kubeadm reset
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
sudo kubeadm init --apiserver-advertise-address=$ipaddress
mkdir -p $HOME/.kube
sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=~/.kube/config
sudo kubectl apply -f http://docs.projectcalico.org/v2.3/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
sudo kubectl taint nodes --all node-role.kubernetes.io/master-
cd
mkdir -p config
sudo cp -f /etc/kubernetes/admin.conf config/admin.conf
sudo chmod 777 config/admin.conf
