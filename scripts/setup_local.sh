#!/bin/bash
# notes:
# 1: install etcd after removing kubernetes.
# 2: check port:  netstat -punta | grep 2379
# 3: #Environment="KUBELET_EXTRA_ARGS=--fail-swap-on=false"

isInstallFromInternet=true
kubernetes_src="/usr/local/go/src/k8s.io/kubernetes"
#kubernetes_src="/home/tanle/go/src/k8s.io/kubernetes"

isAddSource=false

if $isAddSource
then
  sudo bash -c 'apt-get update && apt-get install -y apt-transport-https
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
  cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
  deb http://apt.kubernetes.io/ kubernetes-xenial main
  EOF
  apt-get update'
fi

# remove all kubernetes	 
sudo kubeadm reset
sudo rm -rf $HOME/.kube
sudo rm -rf $HOME/config/admin.conf
sudo apt-get purge -y etcd
sudo apt-get remove -y etcd
sudo apt-get purge -y kubelet kubeadm kubectl kubernetes-cni	
sudo apt-get remove -y kubelet kubeadm kubectl kubernetes-cni
sudo systemctl daemon-reload
# manually uninstall
sudo systemctl stop kubelet 
sudo rm -rf /usr/bin/kube*
sudo rm -rf /etc/systemd/system/kubelet.service
sudo rm -rf /etc/kubernetes/manifests
sudo rm -rf /etc/systemd/system/kubelet.service.d/
sudo rm -rf /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

sudo apt-get install -y etcd
sudo apt-get purge -y etcd


if false
then
  # install docker
  sudo apt-get install -y docker.io
  # add repo for kubernetes
  sudo apt-get update && sudo apt-get install -y apt-transport-https
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
#  sudo cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
#  deb http://apt.kubernetes.io/ kubernetes-xenial main
#  EOF
  sudo apt-get update
fi

if $isInstallFromInternet
then
	sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni
	sudo kubeadm reset # create setting files

	for file in /etc/systemd/system/kubelet.service.d/*-kubeadm.conf
	do
	    echo "Found ${file}"
	    FILE_NAME=$file
	done
	echo "Chosen ${FILE_NAME} as kubeadm.conf"
	sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates="Accelerators=true" /g" $FILE_NAME		
	sudo sed -i -e "s/Environment=\"KUBELET_CERTIFICATE_ARGS=--rotate\-certificates=true /Environment=\"KUBELET_EXTRA_ARGS=--fail-swap-on=false\"\nEnvironment=\"KUBELET_CERTIFICATE_ARGS=--rotate-certificates=true /g" $FILE_NAME  # /etc/systemd/system/kubelet.service.d/10-kubeadm.conf		

	sudo systemctl daemon-reload
	sudo systemctl enable docker
	sudo systemctl start docker
	sudo systemctl enable kubelet
	sudo systemctl start kubelet	

	sudo iptables -F
	sudo swapoff -a
	sudo free -m

	#sudo systemctl status kubelet
#	sudo kubeadm init --skip-preflight-checks --apiserver-advertise-address=localhost
	sudo kubeadm init

	mkdir -p $HOME/.kube
	sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
	sudo chown $(id -u):$(id -g) $HOME/.kube/config
	export KUBECONFIG=$HOME/.kube/config


	sudo kubectl apply -f http://docs.projectcalico.org/v2.3/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
	sudo kubectl taint nodes --all node-role.kubernetes.io/master-	
	mkdir -p ~/config
	sudo cp -f /etc/kubernetes/admin.conf ~/config/admin.conf
	sudo chmod 777 ~/config/admin.conf

else
	echo "install from compiled source  "
	  # need to install docker-ce first.
	# 
	#export KUBERNETES_PROVIDER=local; wget -q -O - https://get.k8s.io | bash
	# http://dougbtv.com/nfvpe/2017/05/12/kubernetes-from-source/
	#find $kubernetes_src | grep gz
	#find $kubernetes_src | grep -iP "(client|server).bin"
	#sudo apt-get install docker-ce

	sudo cp $kubernetes_src/_output/release-stage/client/linux-amd64/kubernetes/client/bin/kubectl /usr/bin/
	sudo cp $kubernetes_src/_output/release-stage/server/linux-amd64/kubernetes/server/bin/kubeadm /usr/bin/
	sudo cp $kubernetes_src/_output/release-stage/server/linux-amd64/kubernetes/server/bin/kubelet /usr/bin/
	sudo cp $kubernetes_src/./build/debs/kubelet.service /etc/systemd/system/kubelet.service
	sudo mkdir -p /etc/kubernetes/manifests
	sudo mkdir -p /etc/systemd/system/kubelet.service.d/
	sudo cp $kubernetes_src/build/debs/10-kubeadm.conf /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

	#vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
	# add these two lines above ExecStart=
	#Environment="KUBELET_AUTHZ_ARGS=--authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt"
	#Environment="KUBELET_CGROUP_ARGS=--cgroup-driver=systemd"

	for file in /etc/systemd/system/kubelet.service.d/*-kubeadm.conf
	do
	    echo "Found ${file}"
	    FILE_NAME=$file
	done
	echo "Chosen ${FILE_NAME} as kubeadm.conf"
	sudo sed -i -e "s/ExecStart=\/usr\/bin\/kubelet /ExecStart=\/usr\/bin\/kubelet --feature-gates="Accelerators=true" /g" $FILE_NAME		
	sudo sed -i -e "s/Environment=\"KUBELET_CERTIFICATE_ARGS=--rotate-certificates=true\"/Environment=\"KUBELET_CERTIFICATE_ARGS=--rotate-certificates=true\"\nEnvironment=\"KUBELET_EXTRA_ARGS=--fail-swap-on=false\"/g" $FILE_NAME

	# Install CNI binaries
	sudo apt-get install kubernetes-cni

	sudo kubeadm reset
	sudo systemctl daemon-reload
	sudo systemctl enable kubelet --now
	sudo systemctl start kubelet

	sudo iptables -F
	sudo swapoff -a
	sudo free -m

  echo " kubeadm init"
	sudo kubeadm init # --skip-preflight-checks
  echo " kubeadm init - end "
  
	mkdir -p $HOME/.kube
	sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
	sudo chown $(id -u):$(id -g) $HOME/.kube/config
	export KUBECONFIG=~/.kube/config

	sudo kubectl apply -f http://docs.projectcalico.org/v2.3/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
  echo "kubectl taint nodes --all node-role.kubernetes.io/master-	"
	sudo kubectl taint nodes --all node-role.kubernetes.io/master-	
	mkdir -p ~/config
	sudo cp -f /etc/kubernetes/admin.conf ~/config/admin.conf
	sudo chmod 777 ~/config/admin.conf
fi
