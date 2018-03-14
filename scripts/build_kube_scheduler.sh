
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

if [ -z "$1" ]
then
	version=1.0
else
	version="$1"
fi

## push to docker.io
if true
then
    #kubernetes_src="/usr/local/go/src/k8s.io/kubernetes"
  kubernetes_src="$HOME/go/src/k8s.io/kubernetes"
  #kubernetes_src="$HOME/go/src/k8s.io/kubernetes-1.9.2"
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
  echo $kubernetes_src $version
fi
# step 1: you have to delete the my-kube-scheduler:1.2 container at the kubernetes server
# - docker images
# - docker rmi 
# step 2: kubectl delete -f my-scheduler.yaml
# step 3: kubectl create -f my-scheduler.yaml
# step 4: 
# kubectl get pods --all-namespaces
# kubectl logs --namespace=kube-system my-scheduler-5b44774d5f-7hjc5