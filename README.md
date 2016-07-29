# Production-grade Kubernetes cluster with logging and monitoring

## Overview

This is a Kubernetes bundle that also includes logging and monitoring. It is
comprised of the following components and features:

- Kubernetes (automating deployment, operations, and scaling containers)
  - Three node Kubernetes cluster with one master and two worker nodes.
  - TLS used for communication between nodes for security.
- Etcd (distributed key value store)
  - Three node cluster for reliability.
- Elastic stack
   - Two nodes for ElasticSearch
   - One node for a Kibana dashboard
   - Beats on every Kubernetes and Etcd node:
     - Filebeat for forwarding logs to ElasticSearch
     - Topbeat for inserting server monitoring data to ElasticSearch

By default this bundle will use whatever the default machine type for your cloud
is, we recommend modifying for proper production use. 

# Usage

## Deploy the bundle

    juju deploy observable-kubernetes

This will deploy the bundle with default constraints. This is useful for lab
environments, however for real-world use you should provide high CPU and memory
instances to kubernetes, you do this by cloning our source repository:

    git clone https://github.com/juju-solutions/bundle-observable-kubernetes.git observable-kubernetes
    cd observable-kubernetes

Then modify `bundle.yaml` to fit your needs, it is commented for your convenience.

    juju deploy .

This bundle exposes the kubernetes and kibana charms by default, meaning those
charms are accessible with public addresses on most clouds. If you would like
to remove external access then run the command `juju unexpose kibana` and
`juju unexpose kubernetes`.

Run `juju status` to get the status of the cluster deployment, we recommend 
doing `watch juju status` in a separate terminal to watch the cluster come up. 

 - etcd should show `(leader) Cluster is healthy`
 - kubernetes should show `Kubernetes running` for each node.

### Alternate deployment methods

This bundle is enabled with an alternate method of deployment called
"conjure-up". Refer to the
[conjure-up documentation](http://conjure-up.io) to learn more.

    sudo apt install conjure-up
    conjure-up cs:~containers/observable-kubernetes to aws

Any of the applications can be scaled out post-deployment. The charms
update the status messages with progress, so it is recommended to run
`watch juju status` to monitor the charm status messages while the cluster is
deployed.

## Download kubectl

After the cluster is deployed you need to download the kubectl binary and
configuration for your cluster from the Kubernetes **master unit** to control
the cluster. To find the master unit check the `juju status` output or run
a command on all kubernetes units to detect the leader:  

    juju run --service kubernetes is-leader

Download the kubectl package from the master unit. Assuming the master is on
unit 0:  

    juju scp kubernetes/0:kubectl_package.tar.gz .
    mkdir kubectl
    tar -xvzf kubectl_package.tar.gz -C kubectl
    cd kubectl

## Control the cluster

You now have the kubectl command and configuration for the cluster that
was just created. There are several ways to specify the configuration for the
kubectl command, using the `--kubeconfig path/to/kubeconfig` is the most
direct. For more information on
[kubectl config](http://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)
see the Kubernetes [user guide](http://kubernetes.io/docs/user-guide/).

To check the state of the cluster:

    ./kubectl cluster-info --kubeconfig ./kubeconfig

Now you can run pods inside the Kubernetes cluster:

    ./kubectl create -f example.yaml --kubeconfig ./kubeconfig

List all pods in the cluster:

    ./kubectl get pods --kubeconfig ./kubeconfig

List all services in the cluster:

    ./kubectl get svc --kubeconfig ./kubeconfig

# Scale out Usage

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
the bundle defaults to three instances in this cluster.

For more scalability, we recommend between 3 and 9 etcd nodes. If you want to
add more nodes:  

    juju add-unit etcd

The CoreOS etcd documentation has a chart for the
[optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

### Scaling Elasticsearch

ElasticSearch is used to hold all the log data and server information logged by
Beats. You can add more Elasticsearch nodes by using the Juju command:

    juju add-unit elasticsearch

## Access Kibana dashboard

The Kibana dashboard can display real time graphs and charts on the details of
the cluster. The Beats charms are sending metrics to the Elasticsearch and
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

 - This bundle is not supported on LXD at this time because Juju needs to use a
LXD profile that can run Docker containers.
 - Destroying the the Kubernetes master unit will result in loss of public key
infrastructure (PKI).
 - No easy way to address the pods from the outside world.
 - The storage feature with ZFS does not work with trusty at this time because
the code has to be enhanced to load the zfs module.

# Contact Information

## Kubernetes details

- [Bundle Source](https://github.com/juju-solutions/bundle-observable-kubernetes)
- [Charm Store](https://jujucharms.com/u/containers/observable-kubernetes/bundle/)
- [Bug tracker](https://github.com/juju-solutions/bundle-observable-kubernetes/issues)
