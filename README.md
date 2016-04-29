# Production-grade Kubernetes cluster with logging and monitoring

## Overview

This is a Kubernetes bundle that also includes logging and monitoring. It is
comprised of the following components and features:

- Kubernetes (automating deployment, operations, and scaling containers)
  - Three node Kubernetes cluster where each unit is a master and a node.  
  - TLS used for communication between nodes for security.
  - ZFS used as a docker datastore for resilience and performance.
- Etcd (distributed key value store)
  - Three node cluster for reliability
- Elastic stack
   - Two nodes for ElasticSearch
   - One node for a Kibana dashboard
   - Beats on every Kubernetes and Etcd node:
     - Filebeat for forwarding logs to ElasticSearch
     - Topbeat for inserting server monitoring data to ElasticSearch

# Usage

    juju deploy cs:~containers/observable-kubernetes

Any of the services provided can be scaled out post-deployment. The charms
update the status messages with progress, so it is recommended to run
`watch juju status` to monitor the cluster coming up. After it is deployed you
need to grab the kubectl and configuration from the Kubernetes leader node to
control the cluster:

    juju scp kubernetes/0:kubectl_package.tar .
    tar zxf kubectl_package.tar
    ./kubectl get pods

You should not have the kubectl command and configuration for the cluster that
was just created, you can now check the state of the cluster:

    ./kubectl cluster-health

Now you can run pods inside the Kubernetes cluster:

    ./kubectl create -f example.yaml

List all pods in the cluster:

    ./kubectl get pods

List all services in the cluster:

    ./kubectl get svc

## Scale out Usage

By default pods are will automatically be spread throughout the Kubernetes
clusters you have deployed.

### Scaling Kubernetes

To add more Kubernetes nodes to the cluster:

    juju add-unit kubernetes

or specify machine constraints to create larger nodes:

    juju add-unit kubernetes --constraints "cpu-cores=8 mem=32G"

Refer to the
[machine constraints documentation](https://jujucharms.com/docs/stable/charms-constraints)
for other machine constraints that might be useful for the Kubernetes nodes.

### Scaling Etcd

Etcd is used as a key-value store for the Kubernetes cluster. For reliability
the cluster defaults to three instances in this bundle.

For more scalability, we recommend between 3 and 9 etcd nodes. If you want to
add more nodes with `juju add-unit etcd`. The CoreOS etcd documentation has a
chart for the [optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

### Scaling Elasticsearch

ElasticSearch is used to hold all the log data and server information logged by Beats. You can add more ES nodes by simply adding more units:

    juju add-unit elasticsearch

## Known Limitations and Issues

 The following issues still need to be resolved with this solution and are being worked on:

 - Killing the the Kubernetes leader will result in loss of cluster PKI.
 - No easy way to address the pods from the outside world
 - ZFS does not work on trusty (a bug that will be fixed soon) yet.

# Contact Information

## Kubernetes details

- [Source](https://github.com/juju-solutions/bundle-observable-kubernetes)
- [Charm Store](https://jujucharms.com/u/containers/observable-kubernetes/bundle/)
- [Bug tracker](https://github.com/juju-solutions/bundle-observable-kubernetes/issues)
