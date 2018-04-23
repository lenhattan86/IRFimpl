#!/bin/bash
# usage:

echo "wait for static"
sleep 5400
## run naivedrf
./install_my_scheduler.sh naivedrf
./install_my_scheduler.sh naivedrf
sleep 15
cd ../experiments/naiveDRF
./main.sh
echo "done naiveDRF"

## run beta estimation 
cd ../beta_estimation
# ls ./profiling.sh
kubectl delete pods --all -n user1
kubectl delete pods --all -n user2
./install_my_scheduler.sh profiling
./install_my_scheduler.sh profiling
sleep 15
./main.sh
echo "remember to save scheduler.log"