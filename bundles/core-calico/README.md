
# Kubernetes Core Bundle

![](https://img.shields.io/badge/release-beta-yellow.svg) ![](https://img.shields.io/badge/kubernetes-1.4.5-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.0+-brightgreen.svg)

## Overview

This is a minimal Kubernetes cluster comprised of the following components and features:

- Kubernetes (automated deployment, operations, and scaling)
     - Two node Kubernetes cluster with one master node and one worker node.
     - TLS used for communication between nodes for security.
     - A CNI plugin (e.g., Flannel)
     - Optional Ingress Controller (on worker)
     - Optional Dashboard addon (on master) including Heapster for cluster monitoring
- EasyRSA
     - Performs the role of a certificate authority serving self signed certificates
       to the requesting units of the cluster.
- Etcd (distributed key value store)
     - One node for basic functionality.

# Usage

This bundle is for small deployments for testing and development. For
multi-node deployments, use the larger
[canonical-kubernetes](http://jujucharms.com/canonical-kubernetes) bundle.

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
juju deploy kubernetes-core
```

> Note: If you desire to deploy this bundle locally on your laptop, see the
> segment about Conjure-Up under Alternate Deployment Methods. Default deployment
> via juju will not properly adjust the apparmor profile to support running
> kubernetes in LXD. At this time, it is a necessary intermediate deployment
> mechanism.

> Note: If you're operating behind a proxy, remember to set the `kubernetes-worker`
proxy configuration options as described in the Proxy configuration section
above.

This bundle exposes the kubernetes-worker charm by default. This means that
it is accessible through its public address.

If you would like to remove external access, unexpose the application:

```
juju unexpose kubernetes-worker
```

To get the status of the deployment, run `juju status`. For a constant update,
this can be used with `watch`.

```
watch -c juju status --color
```

### Alternate deployment methods



#### Usage with your own binaries

In order to support restricted-network deployments, the charms in this bundle
support
[juju resources](https://jujucharms.com/docs/2.0/developer-resources#managing-resources).

This allows you to `juju attach` the resources built for the architecture of
your cloud.

```
juju attach kubernetes-master kubernetes=~/path/to/kubernetes-master.tar.gz
```

#### Interactive deployment using Conjure-up

`conjure-up` is an interactive, terminal UI deployment tool for Juju bundles.
After installing conjure-up, you can deploy the kubernetes-core bundle and tweak config values with one command:

```
sudo apt install conjure-up
conjure-up kubernetes-core
```

Refer to the
[conjure-up documentation](http://conjure-up.io) to learn more.

## Interacting with the Kubernetes cluster

After the cluster is deployed you may assume control over the Kubernetes cluster
from any kubernetes-master, or kubernetes-worker node.

To download the credentials and client application to your local workstation:

Create the kubectl config directory.

```
mkdir -p ~/.kube
```

Copy the kubeconfig to the default location.

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

### Accessing the Kubernetes Dashboard

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
the
[default namespace](http://kubernetes.io/docs/user-guide/namespaces/) of the
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


#### Running the packaged simulation


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


At this point, you can inspect the cluster to observe the workload coming online.

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

#### Clean up microbot

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
for other machine constraints that might be useful for the kubernetes-worker units.


### Scaling Etcd

Etcd is used as a key-value store for the Kubernetes cluster. The bundle
defaults to one instance in this cluster.

For reliability and more scalability, we recommend between 3 and 9 etcd nodes.
If you want to add more nodes:

```
juju add-unit etcd
```

The CoreOS etcd documentation has a chart for the
[optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

## Known Limitations and Issues

 The following are known issues and limitations with the bundle and charm code:

 - Destroying the the easyrsa charm will result in loss of public key
 infrastructure (PKI).

 - Deployment locally on LXD will require the use of conjure-up to tune
   settings on the host's LXD installation to support Docker and other
   componentry.

## Kubernetes details

- [Kubernetes User Guide](http://kubernetes.io/docs/user-guide/)
- [The Canonical Distribution of Kubernetes ](https://jujucharms.com/canonical-kubernetes/bundle/)
- [Bundle Source](https://github.com/juju-solutions/bundle-kubernetes-core)
- [Bug tracker](https://github.com/juju-solutions/bundle-canonical-kubernetes/issues)

# Calico

> Note: this is still in an experimental state. Use at your own risk.

Calico is used as a CNI plugin to manage networking for the Kubernetes cluster.

## Configuration

**ipip**: Enable IP tunneling. *boolean, default false*

**nat-outgoing**: NAT outgoing traffic. *boolean, default true*
