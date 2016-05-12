#!/bin/bash
#
# Description: Download kubectl for controlling Kubernetes Cluster

. /usr/share/conjure-up/hooklib/common.sh

KUBECTL_PATH=$HOME/conjure-up/kubernetes
mkdir -p $KUBECTL_PATH || true

while [ $(unitStatus kubernetes 0) != "active" ]; do sleep 5; done

# TODO: Convert to an actionable item
juju scp kubernetes/0:kubectl_package.tar $KUBECTL_PATH/.
cd $KUBECTL_PATH && tar zxf kubectl_package.tar

exposeResult "Cluster can now be accessed with $KUBECTL_PATH/kubectl application" 0 "true"
