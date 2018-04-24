#!/bin/bash
# usage:

echo "static"
## run naivedrf
./install_my_scheduler.sh static
sleep 5
./install_my_scheduler.sh static
sleep 5
./install_my_scheduler.sh static
sleep 30
cd ../experiments/static
./main.sh
echo "done static"

echo "static2"

./install_my_scheduler.sh static2
sleep 5
./install_my_scheduler.sh static2
sleep 5
./install_my_scheduler.sh static2
sleep 30
cd ../static2
./main.sh
echo "done static2"

echo "naivedrf"
./install_my_scheduler.sh naivedrf
sleep 5
./install_my_scheduler.sh naivedrf
sleep 5
./install_my_scheduler.sh naivedrf
sleep 30
cd ../naiveDRF
./main.sh
echo "done naivedrf"


echo "beta estimation"
./install_my_scheduler.sh profiling
sleep 5
./install_my_scheduler.sh profiling
sleep 5
./install_my_scheduler.sh profiling
sleep 30
cd ../beta_estimation
./main.sh
echo "done beta estimation -- remember to log scheduler."

