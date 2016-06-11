#!/bin/bash

. /usr/share/conjure-up/hooklib/common.sh


services=("etcd" \
          "elasticsearch" \
          "kibana" \
          "kubernetes")

checkUnitsForErrors $services

if [ $(unitStatus kubernetes 0) != "active" ]; then
    exposeResult "Kubernetes is not ready" 0 "false"
fi

exposeResult "Applications ready" 0 "true"
