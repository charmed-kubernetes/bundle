# Production-grade Kubernetes cluster with logging and monitoring

## Overview

This is a Kubernetes bundle that also includes logging and monitoring. It is
comprised of the following components and features:

- Kubernetes (automating deployment, operations, and scaling containers)
  - Three node Kubernetes cluster where each unit is a master and a node.
  - TLS used for communication between nodes for security.
  - ZFS used as a datastore for resilience and performance.
- Etcd (distributed key value store)
  - Three node cluster for reliability.
- Elastic stack
   - Two nodes for ElasticSearch
   - One node for a Kibana dashboard
   - Beats on every Kubernetes and Etcd node:
     - Filebeat for forwarding logs to ElasticSearch
     - Topbeat for inserting server monitoring data to ElasticSearch

# Usage

    juju deploy cs:~containers/observable-kubernetes

Note: This bundle is also conjure-up enabled. Refer to the
[conjure-up documentation](http://conjure-up.io) to learn more.

    sudo apt install conjure-up
    conjure-up cs:~containers/observable-kubernetes to aws

Any of the services provided can be scaled out post-deployment. The charms
update the status messages with progress, so it is recommended to run
`watch juju status` to monitor the cluster coming up.

After the cluster is deployed you need to grab the kubectl binary and
configuration for your cluster from the Kubernetes **master unit** to control
the cluster. To find the master unit check the `juju status` output or run
a command on all kubernetes units to detect the leader:  

    juju run --service kubernetes is-leader

Download the kubectl package from the master unit. Assuming the master is on
unit 0:  

    juju scp kubernetes/0:kubectl_package.tar.gz .
    tar -xvzf kubectl_package.tar.gz -C k8s-charm
    cd k8s-charm

You should now have the kubectl command and configuration for the cluster that
was just created. There are several ways to specify the kubectl configuration
using the `--kubeconfig path/to/kubeconfig` is the most direct. For more
information on
[kubectl config](http://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)
see the Kubernetes [user guide](http://kubernetes.io/docs/user-guide/).

To check the state of the cluster:

    ./kubectl cluster-health --kubeconfig ./kubeconfig

Now you can run pods inside the Kubernetes cluster:

    ./kubectl create -f example.yaml --kubeconfig ./kubeconfig

List all pods in the cluster:

    ./kubectl get pods --kubeconfig ./kubeconfig

List all services in the cluster:

    ./kubectl get svc --kubeconfig ./kubeconfig

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

 - This bundle is not supported on LXD because Juju needs to use a LXD profile
that can run Docker containers.
 - Killing the the Kubernetes master will result in loss of private key
infrastructure (PKI).
 - No easy way to address the pods from the outside world.
 - The storage feature with ZFS does not work with trusty at this time because
the code has to be enhanced to load the zfs module.

# Contact Information

## Kubernetes details

- [Bundle Source](https://github.com/juju-solutions/bundle-observable-kubernetes)
- [Charm Store](https://jujucharms.com/u/containers/observable-kubernetes/bundle/)
- [Bug tracker](https://github.com/juju-solutions/bundle-observable-kubernetes/issues)
