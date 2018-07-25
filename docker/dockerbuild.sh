#!/bin/bash

username="lenhattan86"
repo="ira"

## build TF-GPU
# tagname="gpu"
# docker_file="dockerfilegpu"
# sudo docker rmi $username/$repo:$tagname
# docker build -f $docker_file -t $repo:$tagname .
# docker tag $repo:$tagname $username/$repo:$tagname
# docker push $username/$repo:$tagname

## build TF-CPU
tagname="cpu"
docker_file="dockerfilecpu"
sudo docker rmi $username/$repo:$tagname
docker build -f $docker_file -t $repo:$tagname .
docker tag $repo:$tagname $username/$repo:$tagname
docker push $username/$repo:$tagname