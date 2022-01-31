# The Charmed Distribution of Kubernetes (converged)

![](https://img.shields.io/badge/kubernetes-1.23-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.0+-brightgreen.svg)

## Overview

This is a scaled-out Kubernetes cluster composed of the following components and features:

- Kubernetes (automated deployment, operations, and scaling)
     - Kubernetes cluster with one control-plane and three worker nodes.
     - TLS used for communication between nodes for security.
     - A CNI plugin (Flannel)
     - A load balancer for HA kubernetes-control-plane
     - Optional Ingress Controller (on worker)
     - Optional Dashboard addon (on control-plane) including Heapster for cluster monitoring
- EasyRSA
     - Performs the role of a certificate authority serving self-signed certificates
       to the requesting units of the cluster.
- Etcd (distributed key value store)
     - Three node cluster for reliability.

For a more minimal cluster suitable for development and testing, deploy the smaller
[kubernetes-core](https://jujucharms.com/kubernetes-core) bundle via `conjure-up kubernetes-core`.

# Usage

Installation has been automated via [conjure-up](https://conjure-up.io/):

    sudo snap install conjure-up --classic
    conjure-up charmed-kubernetes

Conjure-up will prompt you for deployment options (AWS, GCE, Azure, etc.) and credentials.

## Proxy configuration

If you are deploying the Charmed Distribution of Kubernetes behind a proxy
(i.e., your charms are running in a limited-egress environment and can not
reach IP addresses external to their network), please refer to the
documentation for
[Proxy configuration](https://github.com/charmed-kubernetes/bundle/wiki/Proxy-configuration).

## Alternate deployment methods

### Deploying with Juju directly

```
juju deploy charmed-kubernetes
```

> Note: If you're deploying on lxd, use conjure-up instead, as described
> above. It configures your lxd profile to support running Kubernetes on lxd.

This will deploy the Charmed Distribution of Kubernetes with default
machine constraints. This is useful for lab environments, but for real-world use
you should provide more CPU and memory to kubernetes-worker units.

You can increase the constraints by downloading and editing the
[bundle.yaml](https://api.jujucharms.com/charmstore/v5/charmed-kubernetes/archive/bundle.yaml)
to fit your needs. Customize the bundle constraints by following [this
guide](https://jujucharms.com/docs/stable/charms-bundles#setting-constraints-in-a-bundle).

To deploy your customized bundle:

```
juju deploy ./bundle.yaml
```

> Note: If you're operating behind a proxy, remember to set the `kubernetes-worker`
proxy configuration options as described in the Proxy configuration section
above.

This bundle exposes the kubeapi-load-balancer and kubernetes-worker charms by
default, so they are accessible through their public addresses.

If you would like to remove external access, unexpose them:

```
juju unexpose kubeapi-load-balancer
juju unexpose kubernetes-worker
```

To get the status of the deployment, run `juju status`. For constant updates,
combine it with the `watch` command:

```
watch -c juju status --color
```

### Using with your own resources

In order to support restricted-network deployments, the charms in this bundle
support
[juju resources](https://jujucharms.com/docs/stable/developer-resources#managing-resources).

This allows you to `juju attach` the resources built for the architecture of
your cloud.

```
juju attach kubernetes-control-plane kubectl=/path/to/kubectl.snap
juju attach kubernetes-control-plane kube-apiserver=/path/to/kube-apiserver.snap
juju attach kubernetes-control-plane kube-controller-manager=/path/to/kube-controller-manager.snap
juju attach kubernetes-control-plane kube-scheduler=/path/to/kube-scheduler.snap
juju attach kubernetes-control-plane cdk-addons=/path/to/cdk-addons.snap

juju attach kubernetes-worker kubectl=/path/to/kubectl.snap
juju attach kubernetes-worker kubelet=/path/to/kubelet.snap
juju attach kubernetes-worker kube-proxy=/path/to/kube-proxy.snap
juju attach kubernetes-worker cni=/path/to/cni.tgz
```

### Using a specific Kubernetes version

You can select a specific version or series of Kubernetes by configuring CDK
to use a specific snap channel. For example, to use the 1.6 series:

```
juju config kubernetes-control-plane channel=1.6/stable
juju config kubernetes-worker channel=1.6/stable
```

After changing the channel, you'll need to manually execute the upgrade action
on each kubernetes-worker and kubernetes-control-plane unit, e.g.:

```
juju run-action kubernetes-control-plane/0 upgrade
...
juju run-action kubernetes-worker/0 upgrade
juju run-action kubernetes-worker/1 upgrade
juju run-action kubernetes-worker/2 upgrade
...
```

By default, the channel is set to `stable` on the current minor version of Kubernetes, for example, `1.6/stable`. This means your cluster will receive automatic upgrades for new patch releases (e.g. 1.6.2 -> 1.6.3), but not for new minor versions (e.g. 1.6.3 -> 1.7). To upgrade to a new minor version, configure the channel manually as described above.


## Interacting with the Kubernetes cluster

After the cluster is deployed you may assume control over the Kubernetes
cluster from any kubernetes-control-plane or kubernetes-worker node.

To download the credentials and client application to your local workstation:

Create the kubectl config directory.

```
mkdir -p ~/.kube
```

Copy the kubeconfig file to the default location.

```
juju scp kubernetes-control-plane/0:config ~/.kube/config
```

Install `kubectl` locally.

```
snap install kubectl --classic
```

Query the cluster.

```
kubectl cluster-info
```

### Accessing the Kubernetes dashboard

The Kubernetes dashboard addon is installed by default, along with Metrics Server,
Heapster, Grafana and InfluxDB for cluster monitoring. The dashboard addons can be
enabled or disabled by setting the `enable-dashboard-addons` config on the
`kubernetes-control-plane` application:

```
juju config kubernetes-control-plane enable-dashboard-addons=true
```

To access the dashboard, you may establish a secure tunnel to your cluster with
the following command:

```
kubectl proxy
```

By default, this establishes a proxy running on your local machine and the
kubernetes-control-plane unit. To reach the Kubernetes dashboard, visit
`http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/` if using 1.16 or newer or 
`http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/` if using an older version.

Logging in to the dashboard will require either a valid kubeconfig or a basic auth
username and password.

### Control the cluster

kubectl is the command line utility to interact with a Kubernetes cluster.


#### Minimal getting started

To check the state of the cluster:

```
kubectl cluster-info
```

List all nodes in the cluster:

```
kubectl get nodes
```

Now you can run pods inside the Kubernetes cluster:

```
kubectl create -f example.yaml
```

List all pods in the cluster:


```
kubectl get pods
```

List all services in the cluster:

```
kubectl get services
```

For expanded information on kubectl beyond what this README provides, please
see the
[kubectl overview](https://kubernetes.io/docs/user-guide/kubectl-overview/)
which contains practical examples and an API reference.

Additionally if you need to manage multiple clusters, there is more information
about configuring kubectl in the
[kubectl config guide](https://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)


### Using Ingress

The kubernetes-worker charm supports deploying an NGINX ingress controller.
Ingress allows access from the Internet to containers running web
services inside the cluster.

First allow the Internet access to the kubernetes-worker charm with with the
following Juju command:

```
juju expose kubernetes-worker
```

In Kubernetes, workloads are declared using pod, service, and ingress
definitions. An ingress controller is provided to you by default and deployed into
the [default namespace](https://kubernetes.io/docs/user-guide/namespaces/) of the
cluster. If one is not available, you may deploy it with:

```
juju config kubernetes-worker ingress=true
```

Ingress resources are DNS mappings to your containers, routed through
[endpoints](https://kubernetes.io/docs/user-guide/services/).

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

Run a Juju action to create the example microbot web application:

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


When all the pods are listed as Running, you are ready to visit the address listed in the HOSTS column of the ingress listing.

> Note: It is normal to see a 502/503 error during initial application deployment.

As you refresh the page, you will be greeted with a microbot web page, serving
from one of the microbot replica pods. Refreshing will show you another
microbot with a different hostname as the requests are load-balanced across
the replicas.

#### Clean up example

There is also an action to clean up the microbot applications. When you are
done using the microbot application you can delete them from the pods with
one Juju action:

```
juju run-action kubernetes-worker/0 microbot delete=true
```

If you no longer need Internet access to your workers, remember to unexpose the
kubernetes-worker charm:

```
juju unexpose kubernetes-worker
```

To learn more about
[Kubernetes Ingress](https://kubernetes.io/docs/user-guide/ingress.html)
and how to configure the Ingress Controller beyond defaults (such as TLS and
websocket support) view the
[nginx-ingress-controller](https://github.com/kubernetes/contrib/tree/master/ingress/controllers/nginx)
project on github.


# Scale out Usage

### Scaling kubernetes-worker

The kubernetes-worker nodes are the load-bearing units of a Kubernetes cluster.

By default, pods are automatically spread across the kubernetes-worker units
that you have deployed.

To add more kubernetes-worker units to the cluster:

```
juju add-unit kubernetes-worker
```

or specify machine constraints to create larger nodes:

```
juju set-constraints kubernetes-worker cpu-cores=8 mem=32G
juju add-unit kubernetes-worker
```

Refer to the
[machine constraints documentation](https://jujucharms.com/docs/stable/charms-constraints)
for other machine constraints that might be useful for the kubernetes-worker units.


### Scaling Etcd

Etcd is the key-value store for the Kubernetes cluster. For reliability
the bundle defaults to three instances in this cluster.

For more scalability, we recommend between 3 and 9 etcd nodes. If you want to
add more nodes:

```
juju add-unit etcd
```

The CoreOS etcd documentation has a chart for the
[optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

# Adding optional storage

Using [Juju Storage](https://jujucharms.com/docs/2.0/charms-storage), the
Charmed Distribution of Kubernetes allows you to connect with durable
storage devices such as [Ceph](https://ceph.com).

Deploy a minimum of three ceph-mon and three ceph-osd charms:
```
juju deploy ceph-mon -n 3
juju deploy ceph-osd -n 3
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
> Different clouds will have different pool names.

Add a storage pool to the ceph-osd charm by NAME,SIZE,COUNT:

```
juju add-storage ceph-osd/0 osd-devices=ebs,10G,1
juju add-storage ceph-osd/1 osd-devices=ebs,10G,1
juju add-storage ceph-osd/2 osd-devices=ebs,10G,1
```

Next relate the storage cluster with the Kubernetes cluster:

```
juju add-relation kubernetes-control-plane ceph-mon
```

We are now ready to enlist
[Persistent Volumes](https://kubernetes.io/docs/user-guide/persistent-volumes/)
in Kubernetes, which our workloads can use via Persistent Volume Claims (PVC).

```
juju run-action kubernetes-control-plane/0 create-rbd-pv name=test size=50
```

This example created a "test" Radios Block Device (rbd) in the size of 50 MB.

You should see the PV become enlisted and be marked as available:
```
$ watch kubectl get pv

NAME CAPACITY   ACCESSMODES   STATUS    CLAIM              REASON    AGE

test   50M          RWO       Available                              10s
```

To consume these Persistent Volumes, your pods will need a
Persistent Volume Claim associated with
them, a task that is outside the scope of this README. See the
[Persistent Volumes](https://kubernetes.io/docs/user-guide/persistent-volumes/)
documentation for more information.

## Known Limitations and Issues

 The following are known issues and limitations with the bundle and charm code:

 - Destroying the easyrsa charm will result in loss of public key
   infrastructure (PKI).

 - Deployment locally on LXD will require the use of conjure-up to tune
   settings on the host's LXD installation to support Docker and other
   components.

 - If resources fail to download during initial deployment for any reason, you
   will need to download and install them manually. For example, if
   kubernetes-control-plane is missing its resources, download them from the resources
   section of the sidebar [here](https://charmhub.io/kubernetes-control-plane/)
   and install them by running, for example:

   `juju attach kubernetes-control-plane kube-apiserver=/path/to/snap`.

   You can find resources for the charmed-kubernetes charms here:

   - [kubernetes-control-plane](https://charmhub.io/kubernetes-control-plane/)
   - [kubernetes-worker](https://charmhub.io/kubernetes-worker/)
   - [easyrsa](https://charmhub.io/easyrsa/)
   - [etcd](https://charmhub.io/etcd/)
   - [flannel](https://charmhub.io/flannel/)

## Charmed Kubernetes Reference

- [Docs](https://www.ubuntu.com/kubernetes/docs)
- [Source Code](https://github.com/charmed-kubernetes)
- [Bug tracker](https://bugs.launchpad.net/charmed-kubernetes)
- [Demos](https://github.com/CanonicalLtd/canonical-kubernetes-demos)
- [Third-party Integrations](https://github.com/CanonicalLtd/canonical-kubernetes-third-party-integrations)
