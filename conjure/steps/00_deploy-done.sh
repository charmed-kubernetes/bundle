#!/bin/bash

. /usr/share/conjure-up/hooklib/common.sh


services=("etcd" \
          "elasticsearch" \
          "kibana" \
          "kubernetes")

checkUnitsForErrors $services
checkUnitsForActive $services

exposeResult "Applications ready" 0 "true"
