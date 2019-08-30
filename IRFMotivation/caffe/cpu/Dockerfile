FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update 
RUN apt install -y git
# RUN apt build-dep caffe-cpu
RUN apt install -y caffe-cpu

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-setuptools \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/lenhattan86/caffe_benchmark/
WORKDIR caffe_benchmark
RUN data/mnist/get_mnist.sh
RUN examples/mnist/create_mnist.sh