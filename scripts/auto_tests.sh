#!/bin/bash
# usage:

sleep 5400
## run naivedrf
./install_my_scheduler.sh naivedrf
./install_my_scheduler.sh naivedrf

cd ../experiments/naiveDRF
# ls ./main.sh

## run beta estimation 
cd ../beta_estimation
# ls ./profiling.sh
kubectl delete pods --all -n user1
kubectl delete pods --all -n user2
./install_my_scheduler.sh profiling
./install_my_scheduler.sh profiling
./main.sh
