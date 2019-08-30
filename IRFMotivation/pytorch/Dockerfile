FROM pytorch/pytorch:nightly-runtime-cuda9.2-cudnn7

RUN apt -y update
RUN apt install -y git

RUN git clone https://github.com/lenhattan86/pytorch-gpu-benchmark
WORKDIR pytorch-gpu-benchmark
RUN ls
RUN pip install -r requirement.txt

# ARG DEBIAN_FRONTEND=noninteractive

# RUN git clone https://github.com/NVIDIA/DeepLearningExamples.git
# WORKDIR DeepLearningExamples/PyTorch/Segmentation/MaskRCNN
# RUN ./download_dataset.sh data

