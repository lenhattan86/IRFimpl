#!/bin/bash
#usage: ./masterkubeup.sh [masterIPaddress]
sudo kubeadm reset -f
# sudo kubeadm reset
if [ -z "$1" ]
then
	ipaddress="128.110.155.25"
else
	ipaddress="$1"
fi

sudo kubeadm reset -f
# sudo kubeadm reset
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
# enable GPU for kubectl version < 1.10
# sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates="Accelerators=true" /g" $FILE_NAME
# sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates=PodPriority=true --feature-gates="Accelerators=true" /g" $FILE_NAME
# sudo systemctl daemon-reload
# sudo systemctl restart kubelet

sudo kubeadm reset -f
# sudo kubeadm reset
sudo kubeadm init  --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=$ipaddress

mkdir -p $HOME/.kube; sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config; sudo chown $(id -u):$(id -g) $HOME/.kube/config; export KUBECONFIG=~/.kube/config

# old
#sudo kubectl apply -f http://docs.projectcalico.org/v2.3/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
# 1.9
#kubectl apply -f https://docs.projectcalico.org/v3.0/getting-started/kubernetes/installation/hosted/kubeadm/1.7/calico.yaml 
# 1.11
sudo kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
sudo kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml

sudo kubectl taint nodes --all node-role.kubernetes.io/master-; mkdir -p $HOME//config; sudo cp -f /etc/kubernetes/admin.conf  $HOME//config/admin.conf; sudo chmod 777  $HOME//config/admin.conf

## install metrics-server for resource usage monitoring// metrics-server is not mature
# git checkout https://github.com/kubernetes-incubator/metrics-server
# 
