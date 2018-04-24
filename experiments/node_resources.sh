#!/bin/bash

stopTime=$1
logFile=$2

set -euo pipefail
nodes=$(kubectl get node --no-headers -o custom-columns=NAME:.metadata.name)

for node in $nodes; do
  echo "Node: $node"
  kubectl describe node "$node" | sed '1,/Non-terminated Pods/d'  
done