#!/bin/bash
#
# Description: Download kubectl for controlling Kubernetes Cluster

. /usr/share/conjure-up/hooklib/common.sh

KUBECTL_PATH=$HOME/conjure-up/kubernetes
mkdir -p $KUBECTL_PATH || true

if [ $(unitStatus kubernetes 0) = "error" ]; then
    exposeResult "There is an error with the kubernetes service, plese check juju status." 1 "false"
fi

if [ $(unitStatus etcd 0) = "error" ]; then
    exposeResult "There is an error with the etcd service, plese check juju status." 1 "false"
fi

if [ $(unitStatus kubernetes 0) != "active" ]; then
    exposeResult "Kubernetes is not quite ready yet" 0 "false"
fi

# TODO: Convert to an actionable item
juju scp kubernetes/0:kubectl_package.tar $KUBECTL_PATH/.
cd $KUBECTL_PATH && tar zxf kubectl_package.tar

exposeResult "Cluster can now be accessed with $KUBECTL_PATH/kubectl application" 0 "true"
