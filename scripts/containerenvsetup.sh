#!/bin/bash
export PATH=/usr/local/cuda-8.0/targets/x86_64-linux/lib/stubs${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/nvidia${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-8.0/targets/x86_64-linux/lib/stubs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
cd 
rm -rf benchmarks
#git clone https://github.com/tensorflow/benchmarks
#git clone https://github.com/swiftdiaries/benchmarks
#cd benchmarks/scripts/tf_cnn_benchmarks
rm -rf tf_bench
git clone https://github.com/lenhattan86/tf_bench
cd tf_bench/scripts/tf_cnn_benchmarks

python tf_cnn_benchmarks.py --device=cpu --local_parameter_device=cpu --model=alexnet --num_gpus=1
#python tf_cnn_benchmarks.py --device=cpu --local_parameter_device=cpu --model=vgg16 --num_gpus=36
#python tf_cnn_benchmarks.py --device=cpu --local_parameter_device=cpu --model=inception3 --num_gpus=36
#python tf_cnn_benchmarks.py --device=cpu --local_parameter_device=cpu --model=resnet50 --num_gpus=36

#python tf_cnn_benchmarks.py --device=gpu --local_parameter_device=cpu --model=alexnet --num_gpus=2
#python tf_cnn_benchmarks.py --device=gpu --local_parameter_device=cpu --model=vgg16 --num_gpus=2
#python tf_cnn_benchmarks.py --device=gpu --local_parameter_device=cpu --model=inception3 --num_gpus=1
#python tf_cnn_benchmarks.py --device=gpu --local_parameter_device=cpu --model=resnet50 --num_gpus=1


