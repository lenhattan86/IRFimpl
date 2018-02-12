
## TEST
# build kubescheduler -> doesn't work well

# make all WHAT='plugin/cmd/kube-scheduler'

# go build k8s.io/kubernetes/plugin/cmd/kube-scheduler
 
## from Adhita
if false
then
  wget https://dl.k8s.io/v1.8.0/kubernetes.tar.gz
  tar -C -zvf sourcekubernetes/ kubernetes.tar.gz
  cd sourcekubernetes/
  docker build -t my-kube-scheduler:1.0 .
  docker tag my-kube-scheduler:1.0 swiftdiaries/my-kube-scheduler:1.0
  docker push swiftdiaries/my-kube-scheduler:1.0
  kubectl create -f my-scheduler.yaml
  kubectl get pods --namespace=kube-system
fi

## push to gcloud
if false
then
  #kubernetes_src="/usr/local/go/src/k8s.io/kubernetes"
  kubernetes_src="$HOME/go/src/k8s.io/kubernetes"
# https://kubernetes.io/docs/tasks/administer-cluster/configure-multiple-schedulers/
# Dockfile
# FROM busybox
# ADD ./_output/dockerized/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler
echo "FROM busybox
ADD ./_output/dockerized/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler" > $kubernetes_src/Dockerfile
  docker build -t my-kube-scheduler:1.0 $kubernetes_src
  docker tag my-kube-scheduler:1.0 gcr.io/kube-scheduler/my-kube-scheduler:1.0
  # images may disappear before this command
  gcloud docker -- push gcr.io/kube-scheduler/my-kube-scheduler:1.0
  # upload my scheduler
  kubectl delete -f my-scheduler.yaml
  kubectl create -f my-scheduler.yaml
fi

## push to docker.io
if true
then
  version=1.2
  #kubernetes_src="/usr/local/go/src/k8s.io/kubernetes"
  kubernetes_src="$HOME/go/src/k8s.io/kubernetes"
#  kubernetes_src="$HOME/go/src/k8s.io/kubernetes-1.9.2"
# https://kubernetes.io/docs/tasks/administer-cluster/configure-multiple-schedulers/
# Dockfile
# FROM busybox
# ADD ./_output/dockerized/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler
echo "FROM busybox
ADD ./_output/dockerized/bin/linux/amd64/kube-scheduler /usr/local/bin/kube-scheduler" > $kubernetes_src/Dockerfile
  docker build -t my-kube-scheduler:$version $kubernetes_src
  docker tag my-kube-scheduler:$version lenhattan86/my-kube-scheduler:$version
  # images may disappear before this command
  docker push lenhattan86/my-kube-scheduler:$version
  # upload my scheduler
#  kubectl delete -f my-scheduler.yaml
#  kubectl create -f my-scheduler.yaml
echo $kubernetes_src $version
fi

