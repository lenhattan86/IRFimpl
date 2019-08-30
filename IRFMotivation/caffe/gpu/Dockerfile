FROM nvidia/cuda:9.2-cudnn7-devel-ubuntu18.04
# FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update 
RUN apt install -y git
RUN apt install -y caffe-cuda

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

# work around to fix nvidia driver/library mismatch.
# RUN apt install -y lsof
# RUN lsof /dev/nvidia*
# RUN rmmod nvidia_drm
# RUN rmmod nvidia_modeset
# RUN rmmod nvidia_uvm
