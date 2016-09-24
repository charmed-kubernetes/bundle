#!/bin/sh

set +ex

# This is for deploying local charms, and attaching local resources. How
# you obtain these resources is up to the operator

juju attach kubernetes-master kubernetes=~/resources/kubernetes-master.tar.gz
juju attach kubernetes-worker kubernetes=~/resources/kubernetes-worker.tar.gz
juju attach flannel flannel=~/resources/flannel-v0.6.1-linux-amd64.tar.gz
juju attach easyrsa easyrsa=~/resources/EasyRSA-3.0.1.tgz


