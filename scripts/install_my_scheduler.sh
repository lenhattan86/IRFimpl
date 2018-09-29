if [ -z "$1" ]
then
	version=1.0
else
	version="$1"
fi
kubectl delete pods --all --grace-period=0 --force
kubectl delete pods --all -n user1 --grace-period=0 --force
kubectl delete pods --all -n user2 --grace-period=0 --force
kubectl delete pods --all -n user3 --grace-period=0 --force
kubectl delete pods --all -n user4 --grace-period=0 --force
kubectl delete pods --all -n user5 --grace-period=0 --force
kubectl delete pods --all -n user6 --grace-period=0 --force
kubectl delete pods --all -n user7 --grace-period=0 --force
kubectl delete pods --all -n user8 --grace-period=0 --force

yamlFile="my-scheduler.yaml"
kubectl delete -f $yamlFile
#sudo docker images
#echo "Enter my-scheduler $version image id: "
#read image_id
#sudo docker rmi -f $image_id

echo '...'
sleep 15 # wait for docker completely removes the image.
echo "remove the local images"
sudo docker rmi lenhattan86/my-kube-scheduler:$version -f
#echo "pull the latest version online"
sudo docker pull lenhattan86/my-kube-scheduler:$version

echo "apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    component: scheduler
    tier: control-plane
  name: my-scheduler
  namespace: kube-system
spec:
  selector:
    matchLabels:
      component: scheduler
      tier: control-plane
  replicas: 1
  template:
    metadata:
      labels:
        component: scheduler
        tier: control-plane
        version: second
    spec:
      containers:
      - command:
        - /usr/local/bin/kube-scheduler
        - --address=0.0.0.0
        - --leader-elect=false
        - --scheduler-name=my-scheduler
        image: lenhattan86/my-kube-scheduler:$version
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10251
          initialDelaySeconds: 15
        name: kube-second-scheduler
        readinessProbe:
          httpGet:
            path: /healthz
            port: 10251
        resources:
          requests:
            cpu: '0.1'
        securityContext:
          privileged: false
        volumeMounts: []
      hostNetwork: false
      hostPID: false
      volumes: []" > $yamlFile

kubectl create clusterrolebinding --user system:serviceaccount:kube-system:default kube-system-cluster-admin --clusterrole cluster-admin
kubectl create -f $yamlFile

# kubectl delete -f $yamlFile
# sleep 10
# sudo docker rmi lenhattan86/my-kube-scheduler:$version
# kubectl create -f $yamlFile

sleep 3
kubectl get pods -n kube-system

echo "kubectl logs --namespace=kube-system [pod name]"
# kubectl get pods --all-namespaces --field-selector=status.phase==Running
date