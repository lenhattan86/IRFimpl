echo "./install_my_scheduler.sh version"
if [ -z "$1" ]
then
	version=1.2
else
	version="$1"
fi

yamlFile="my-scheduler.yaml"
kubectl delete -f $yamlFile
sleep 15
docker images
echo "Enter my-scheduler $version image id: "
read image_id
sudo docker rmi $image_id

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

kubectl create -f $yamlFile
kubectl get pods --all-namespaces
echo "kubectl get pods --all-namespaces"
echo "kubectl logs --namespace=kube-system [pod name]"