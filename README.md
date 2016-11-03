# The Canonical Distribution of Kubernetes

![](https://img.shields.io/badge/release-beta-yellow.svg) ![](https://img.shields.io/badge/kubernetes-1.4.5-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.0+-brightgreen.svg)

## Overview

This is a Kubernetes cluster that includes logging, monitoring, and operational
knowledge. It is comprised of the following components and features:

- Kubernetes (automated deployment, operations, and scaling)
     - Three node Kubernetes cluster with one master and two worker nodes.
     - TLS used for communication between nodes for security.
     - Flannel Software Defined Network (SDN) plugin
     - A load balancer for HA kubernetes-master (Experimental)
     - Optional Ingress Controller (on worker)
     - Optional Dashboard addon (on master) including Heapster for cluster monitoring
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

## Proxy configuration

If you are operating behind a proxy (i.e., your charms are running in a
limited-egress environment and can not reach IP addresses external to their
network), you will need to configure your model appropriately before deploying
the Kubernetes bundle.

First, configure your model's `http-proxy` and `https-proxy` settings with your
proxy (here we use `squid.internal:3128` as an example):

```sh
$ juju model-config http-proxy=http://squid.internal:3128 https-proxy=https://squid.internal:3128
```

Because services often need to reach machines on their own network (including
themselves), you will also need to add `localhost` to the `no-proxy` model
configuration setting, along with any internal subnets you're using. The
following example includes two subnets:

```sh
$ juju model-config no-proxy=localhost,10.5.5.0/24,10.246.64.0/21
```

After deploying the bundle, you need to configure the `kubernetes-worker` charm
to use your proxy:

```sh
$ juju config kubernetes-worker http_proxy=http://squid.internal:3128 https_proxy=https://squid.internal:3128
```

## Deploy the bundle

```
juju deploy canonical-kubernetes
```

This will deploy the Canonical Distribution of Kubernetes offering with default
constraints. This is useful for lab environments, however for real-world use
you should provide higher CPU and memory instances to kubernetes-worker units.

You can increase the constraints by editing the
[bundle.yaml](https://github.com/juju-solutions/bundle-canonical-kubernetes)
to fit your needs by removing the `#` comment character.

```
juju deploy ./bundle.yaml
```

> Note: If you're operating behind a proxy, remember to set the `kubernetes-worker`
proxy configuration options as described in the Proxy configuration section
above.

This bundle exposes the kubeapi-load-balancer and kibana charms by default
This means those charms are accessible through their public addresses.

If you would like to remove external access, unexpose the applications:

```
juju unexpose kibana
juju unexpose kubeapi-load-balancer
```

To get the status of the deployment, run `juju status`. For a constant update,
this can be used with `watch`.

```
watch -c juju status --color
```

## Alternate deployment methods


### Deploy with your own binaries

In order to support restricted-network deployments, the charms in this bundle
support
[juju resources](https://jujucharms.com/docs/2.0/developer-resources#managing-resources).

This allows you to `juju attach` the resources built for the architecture of
your cloud.

```
juju attach kubernetes-master kubernetes=~/path/to/kubernetes-master.tar.gz
```

### Interactive deployment using Conjure-up

`conjure-up` is an interactive, terminal UI deployment tool for Juju bundles.
After installing conjure-up, you can deploy the canonical-kubernetes bundle and
tweak config values with one command:

```
sudo apt install conjure-up
conjure-up canonical-kubernetes
```

Refer to the
[conjure-up documentation](http://conjure-up.io) to learn more.

## Interacting with the Kubernetes cluster

After the cluster is deployed you may assume control over the Kubernetes 
cluster from any kubernetes-master, or kubernetes-worker node.

To download the credentials and client application to your local workstation:

Create the kubectl config directory.

```
mkdir -p ~/.kube
```

Copy the kubeconfig file to the default location.

```
juju scp kubernetes-master/0:config ~/.kube/config
```

Fetch a binary for the architecture you have deployed. If your client is a
different architecture you will need to get the appropriate `kubectl` binary
through other means.

```
juju scp kubernetes-master/0:kubectl ./kubectl
```

Query the cluster.

```
./kubectl cluster-info
```

### Accessing the Kubernetes dashboard

The Kubernetes dashboard addon is installed by default, along with Heapster,
Grafana and InfluxDB for cluster monitoring. The dashboard addons can be
enabled or disabled by setting the `enable-dashboard-addons` config on the
`kubernetes-master` application:

```
juju config kubernetes-master enable-dashboard-addons=true
```

To access the dashboard, you may establish a secure tunnel to your cluster with
the following command:

```
./kubectl proxy
```

By default, this establishes a proxy running on your local machine and the
kubernetes-master unit. To reach the Kubernetes dashboard, visit
`http://localhost:8001/ui`

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
./kubectl get services
```

For expanded information on kubectl beyond what this README provides, please
see the
[kubectl overview](http://kubernetes.io/docs/user-guide/kubectl-overview/)
which contains practical examples and an API reference.

Additionally if you need to manage multiple clusters, there is more information
about configuring kubectl with the
[kubectl config guide](http://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)


### Using Ingress

The kubernetes-worker charm supports deploying an NGINX ingress controller.
Ingress allows access from the Internet to containers inside the cluster
running web services.

First allow the Internet access to the kubernetes-worker charm with with the
following Juju command:

```
juju expose kubernetes-worker
```

In Kubernetes, workloads are declared using pod, service, and ingress
definitions. An ingress controller is provided to you by default, deployed into
the [default namespace](http://kubernetes.io/docs/user-guide/namespaces/) of the
cluster. If one is not available, you may deploy this with:

```
juju config kubernetes-worker ingress=true
```

Ingress resources are DNS mappings to your containers, routed through
[endpoints](http://kubernetes.io/docs/user-guide/services/)

As an example for users unfamiliar with Kubernetes, we packaged an action to
both deploy an example and clean itself up.

To deploy 5 replicas of the microbot web application inside the Kubernetes
cluster run the following command:

```
juju run-action kubernetes-worker/0 microbot replicas=5
```

This action performs the following steps:

- It creates a deployment titled 'microbots' comprised of 5 replicas defined
during the run of the action. It also creates a service named 'microbots'
which binds an 'endpoint', using all 5 of the 'microbots' pods.

- Finally, it will create an ingress resource, which points at a
[xip.io](https://xip.io) domain to simulate a proper DNS service.


#### Running the packaged example

You can run a Juju action to create an example microbot web application:

    $ juju run-action kubernetes-worker/0 microbot replicas=3
    Action queued with id: db7cc72b-5f35-4a4d-877c-284c4b776eb8

    $ juju show-action-output db7cc72b-5f35-4a4d-877c-284c4b776eb8
    results:
      address: microbot.104.198.77.197.xip.io
    status: completed
    timing:
      completed: 2016-09-26 20:42:42 +0000 UTC
      enqueued: 2016-09-26 20:42:39 +0000 UTC
      started: 2016-09-26 20:42:41 +0000 UTC

> **Note**: Your FQDN will be different and contain the address of the cloud 
> instance.

At this point, you can inspect the cluster to observe the workload coming
online.

#### List the pods


    $ kubectl get pods
    NAME                             READY     STATUS    RESTARTS   AGE
    default-http-backend-kh1dt       1/1       Running   0          1h
    microbot-1855935831-58shp        1/1       Running   0          1h
    microbot-1855935831-9d16f        1/1       Running   0          1h
    microbot-1855935831-l5rt8        1/1       Running   0          1h
    nginx-ingress-controller-hv5c2   1/1       Running   0          1h



#### List the services and endpoints

    $ kubectl get services,endpoints
    NAME                       CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
    svc/default-http-backend   10.1.225.82   <none>        80/TCP    1h
    svc/kubernetes             10.1.0.1      <none>        443/TCP   1h
    svc/microbot               10.1.44.173   <none>        80/TCP    1h
    NAME                      ENDPOINTS                               AGE
    ep/default-http-backend   10.1.68.2:80                            1h
    ep/kubernetes             172.31.31.139:6443                      1h
    ep/microbot               10.1.20.3:80,10.1.68.3:80,10.1.7.4:80   1h


#### List the ingress resources

    $ kubectl get ingress
    NAME               HOSTS                          ADDRESS         PORTS     AGE
    microbot-ingress   microbot.52.38.62.235.xip.io   172.31.26.109   80        1h


When all the pods are listed as Running, the endpoint has more than one host
you are ready to visit the address in the hosts section of the ingress listing.

It is normal to see a 502/503 error during initial application turnup.

As you refresh the page, you will be greeted with a microbot web page, serving
from one of the microbot replica pods. Refreshing will show you another
microbot with a different hostname, as the requests are load balanced through
out the replicas.

#### Clean up example

There is also an action to clean up the microbot applications. When you are
done using the microbot application you can delete them from the pods with
one Juju action:

```
juju run-action kubernetes-worker/0 microbot delete=true
```

If you no longer need Internet access to your workers remember to unexpose the
kubernetes-worker charm:

```
juju unexpose kubernetes-worker
```

To learn more about
[Kubernetes Ingress](http://kubernetes.io/docs/user-guide/ingress.html)
and how to really tune the Ingress Controller beyond defaults (such as TLS and
websocket support) view the
[nginx-ingress-controller](https://github.com/kubernetes/contrib/tree/master/ingress/controllers/nginx)
project on github.


# Scale out Usage

Any of the applications can be scaled out post-deployment. The charms
update the status messages with progress, so it is recommended to run.

```
watch -c juju status --color
```

### Scaling kubernetes-worker

The kubernetes-worker nodes are the load-bearing units of a Kubernetes cluster.

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
for other machine constraints that might be useful for the kubernetes-worker
units.


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

# Adding optional storage

The Canonical Distribution of Kubernetes allows you to connect with durable
storage devices such as [Ceph](http://ceph.com). When paired with the
[Juju Storage](https://jujucharms.com/docs/2.0/charms-storage) feature you
can add durable storage easily and across most public clouds.

Deploy a minimum of three ceph-mon and three ceph-osd charms.

```
juju deploy cs:ceph-mon -n 3
juju deploy cs:ceph-osd -n 3
```

Relate the charms:
```
juju add-relation ceph-mon ceph-osd
```

List the storage pools available to Juju for your cloud:

```
$ juju storage-pools
Name     Provider  Attrs
ebs      ebs       
ebs-ssd  ebs       volume-type=ssd
loop     loop      
rootfs   rootfs    
tmpfs    tmpfs
```
> **Note**: This listing is for the Amazon Web Services public cloud.
> Different clouds may have different pool names.

Add a storage pool to the ceph-osd charm by NAME,SIZE,COUNT:

```
juju add-storage ceph-osd/0 osd-devices=ebs,10G,1
juju add-storage ceph-osd/1 osd-devices=ebs,10G,1
juju add-storage ceph-osd/2 osd-devices=ebs,10G,1
```

Next relate the storage cluster with the Kubernetes cluster:

```
juju add-relation kubernetes-master ceph-mon
```

We are now ready to enlist 
[Persistent Volumes](http://kubernetes.io/docs/user-guide/persistent-volumes/)
in Kubernetes which our workloads can consume via Persistent Volume (PV) claims.

```
juju run-action kubernetes-master/0 create-rbd-pv name=test size=50
```

This example created a "test" Radios Block Device (rbd) in the size of 50 MB.

Use watch on your Kubernetes cluster like the following, you should see the PV
become enlisted and be marked as available:

```
$ watch kubectl get pv

NAME CAPACITY   ACCESSMODES   STATUS    CLAIM              REASON    AGE

test   50M          RWO       Available                              10s
```

To consume these Persistent Volumes, your pods will need an associated
Persistant Volume Claim with
them, and is outside the scope of this README. See the
[Persistant Volumes](http://kubernetes.io/docs/user-guide/persistent-volumes/)
documentation for more information.

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

 - kubernetes-master, kubernetes-worker, kubeapi-load-balancer and etcd are not
 supported on LXD at this time.
 - Destroying the the easyrsa charm will result in loss of public key
 infrastructure (PKI).

## Kubernetes details

- [Kubernetes User Guide](http://kubernetes.io/docs/user-guide/)
- [The Canonical Distribution of Kubernetes ](https://jujucharms.com/canonical-kubernetes/bundle/)
- [Bundle Source](https://github.com/juju-solutions/bundle-canonical-kubernetes)
- [Bug tracker](https://github.com/juju-solutions/bundle-canonical-kubernetes/issues)
