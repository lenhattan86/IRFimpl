#!/bin/bash

username="lenhattan86"
repo="ira"

## build TF-CPU
tagname="cpu"
docker_file="dockerfilecpu"
sudo docker rmi -f $repo:$tagname --force
sudo docker rmi -f $username/$repo:$tagname --force
docker build -f $docker_file -t $repo:$tagname .
docker tag $repo:$tagname $username/$repo:$tagname
docker push $username/$repo:$tagname

## build TF-GPU
tagname="gpu"
docker_file="dockerfilegpu"
sudo docker rmi -f $repo:$tagname --force
sudo docker rmi -f $username/$repo:$tagname --force
docker build -f $docker_file -t $repo:$tagname .
docker tag $repo:$tagname $username/$repo:$tagname
docker push $username/$repo:$tagname