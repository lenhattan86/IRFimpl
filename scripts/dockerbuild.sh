#!/bin/bash
#Usage: ./dockerbuild.sh tagname username

if [ -z "$1" ]
then
	tagname="gpu"
	#tagname="cpu"
else
	tagname="$1"
fi

if [ -z "$2" ]
then
	username="lenhattan86"
else
	username="$2"
fi

if [ -z "$3" ]
then
	docker_file="Dockerfile"
	#docker_file="dockerfilecpu"
else
	docker_file="$3"
fi

docker build -f $docker_file -t $tagname .
docker tag $tagname $username/$tagname
docker push $username/$tagname
# errors:
# Temporary failure resolving 'archive.ubuntu.com' -> docker version