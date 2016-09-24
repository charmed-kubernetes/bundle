# Canonical Kubernetes

![](https://img.shields.io/badge/release-beta-yellow.svg) ![](https://img.shields.io/badge/kubernetes-1.4.0-beta10-brightgreen.svg) ![](https://img.shields.io/badge/juju-1.25+-brightgreen.svg)

## Overview

This is a Kubernetes cluster that includes logging, monitoring, and operational
knowledge. It is comprised of the following components and features:

- Kubernetes (automated deployment, operations, and scaling)
  - Three node Kubernetes cluster with one master and two worker nodes.
  - TLS used for communication between nodes for security.
  - Flannel networking plugin
  - A load balancer for HA kubernetes-master (Experimental)
- EasyRSA
  - Performs the role of a certificate authority serving self signed certificates
    to the requesting units of the cluster.
- Etcd (distributed key value store)
  - Three node cluster for reliability.
- Elastic stack
   - Two nodes for ElasticSearch
   - One node for a Kibana dashboard
   - Beats on every Kubernetes and Etcd node:
     - Filebeat for forwarding logs to ElasticSearch
     - Topbeat for inserting server monitoring data to ElasticSearch

# Usage

This bundle is for multi-node deployments, for individual deployments for
developers, use the smaller
[kubernetes-core](http://jujucharms.com/kubernetes-core) bundle.

## Deploy the bundle

```
juju deploy canonical-kubernetes
```

This will deploy the Canonical Kubernetes offering with default constraints.
This is useful for lab environments, however for real-world use you should
provide high CPU and memory instances to kubernetes-worker.

You can do this by editing the [bundle](https://github.com/juju-solutions/bundle-canonical-kubernetes)
to fit your needs, it is commented for your convenience.

```
juju deploy ./bundle.yaml
```

This bundle exposes the kubeapi-load-balancer and kibana applications by default.
This means those charms are accessible through the public addresses.

If you would like to remove external access, unexpose the applications:

```
juju unexpose kibana
juju unexpose kubernetes
```

To get the status of the deployment, run `juju status`. For a constant update,
this can be used with `watch`.

```
watch -c juju status --color
```
### Alternate deployment methods

#### Usage with your own binaries

In order to support restricted-network deployments, the charms in this bundle
support [juju resources](https://jujucharms.com/docs/2.0/developer-resources#managing-resources).

This allows you to `juju attach` the resources built for the architecture of
your cloud.

```
juju attach kubernetes-master kubernetes=~/path/to/kubernetes-master.tar.gz
```

#### Conjure Up

This bundle is enabled with an alternate method via `conjure-up`, a big
software installer. Refer to the
[conjure-up documentation](http://conjure-up.io) to learn more.

```
sudo apt install conjure-up
conjure-up canonical-kubernetes
```

## Interacting with the Kubernetes cluster

After the cluster is deployed you may assume control over the Kubernetes cluster
from any kubernetes-master, or kubernetes-worker node.

To download the credentials and client application to your local workstation:

```
# Create the kubectl config directory.
mkdir -p ~/.kube

# Copy the kubeconfig to the default location.
juju scp kubernetes-master/0:config ~/.kube/config

# Fetch a binary for the architecture you have deployed.
juju scp kubernetes-master/0:kubectl ./kubectl

# Query the cluster.
./kubectl cluster-info

```

### Control the cluster

kubectl is the command line utility to interact with a Kubernetes cluster.


#### Minimal getting started

To check the state of the cluster:

```
./kubectl cluster-info
```

List all nodes in the cluster:

```
./kubectl get nodes
```

Now you can run pods inside the Kubernetes cluster:

```
./kubectl create -f example.yaml
```

List all pods in the cluster:


```
./kubectl get pods
```

List all services in the cluster:

```
./kubectl get svc
```

For expanded information on kubectl beyond what this README provides, please
see the [kubectl overview](http://kubernetes.io/docs/user-guide/kubectl-overview/)
which contains practical examples and an API reference.

Additionally if you need to manage multiple clusters, there is more information
about configuring kubectl with the
[kubectl config guide](http://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)



# Scale out Usage

Any of the applications can be scaled out post-deployment. The charms
update the status messages with progress, so it is recommended to run.

```
watch -c juju status --color
```


### Scaling kubernetes-worker

kubernetes-worker nodes are the load-bearing units of a Kubernetes cluster.

By default pods are automatically spread throughout the kubernetes-worker units
that you have deployed.

To add more kubernetes-worker units to the cluster:

```
juju add-unit kubernetes-worker
```

or specify machine constraints to create larger nodes:

```
juju add-unit kubernetes-worker --constraints "cpu-cores=8 mem=32G"
```

Refer to the
[machine constraints documentation](https://jujucharms.com/docs/stable/charms-constraints)
for other machine constraints that might be useful for the kubernetes-worker units.


### Scaling Etcd

Etcd is used as a key-value store for the Kubernetes cluster. For reliability
the bundle defaults to three instances in this cluster.

For more scalability, we recommend between 3 and 9 etcd nodes. If you want to
add more nodes:  

```
juju add-unit etcd
```

The CoreOS etcd documentation has a chart for the
[optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

### Scaling Elasticsearch

ElasticSearch is used to hold all the log data and server information logged by
Beats. You can add more Elasticsearch nodes by using the Juju command:

```
juju add-unit elasticsearch
```

## Accessing the Kibana dashboard

The Kibana dashboard can display real time graphs and charts on the details of
the cluster. The Beats charms are sending metrics to Elasticsearch and
Kibana displays the data with graphs and charts.

Get the charm's public address from the `juju status` command.

* Access Kibana by browser:  http://KIBANA_IP_ADDRESS/
* Select the index pattern that you want as default from the left menu.
  * Click the green star button to make this index a default.
* Select "Dashboard" from the Kibana header.
  * Click the open folder icon to Load a Saved Dashboard.
* Select the "Topbeat Dashboard" from the left menu.

![Setup Kibana](http://i.imgur.com/tgYFSjM.gif)


## Known Limitations and Issues

 The following are known issues and limitations with the bundle and charm code:

 - kubernetes-worker is not supported on LXD at this time.
 - Destroying the the easyrsa charm will result in loss of public key
 infrastructure (PKI).
 - No easy way to address the pods from the outside world.

## Kubernetes details

- [User Guide](http://kubernetes.io/docs/user-guide/).
- [Charm Store](https://jujucharms.com/canonical-kubernetes/bundle/)
- [Bundle Source](https://github.com/juju-solutions/bundle-canonical-kubernetes)
- [Bug tracker](https://github.com/juju-solutions/bundle-canonical-kubernetes/issues)
