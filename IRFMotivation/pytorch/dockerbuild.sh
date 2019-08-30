tag="1.0"
docker rmi pytorch:$tag
docker rmi lenhattan86/pytorch:$tag
docker build -t pytorch:$tag .
docker tag pytorch:$tag lenhattan86/pytorch:$tag
docker push lenhattan86/pytorch:$tag