tag="cpu"
docker rmi caffe:$tag
docker rmi lenhattan86/caffe:$tag
docker build -t caffe:$tag .
docker tag caffe:$tag lenhattan86/caffe:$tag
docker push lenhattan86/caffe:$tag