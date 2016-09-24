#!/bin/sh

set +ex

# This is for deploying local charms, and attaching local resources. How
# you obtain these resources is up to the operator

echo "Attaching kubernetes-master"
juju attach kubernetes-master kubernetes=$HOME/resources/kubernetes-master.tar.gz
echo "Attaching kubernetes-worker"
juju attach kubernetes-worker kubernetes=$HOME/resources/kubernetes-worker.tar.gz
echo "Attaching flannel" 
juju attach flannel flannel=$HOME/resources/flannel-v0.6.1-linux-amd64.tar.gz
echo "Attaching easyrsa"
juju attach easyrsa easyrsa=$HOME/resources/EasyRSA-3.0.1.tgz


