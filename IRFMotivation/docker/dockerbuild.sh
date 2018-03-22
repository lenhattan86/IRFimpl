#!/bin/bash
#Usage: ./dockerbuild.sh tagname username
docker build --no-cache -t $1 .
docker tag $1 $2/$1
docker push $2/$1
