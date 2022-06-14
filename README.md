![CK logo](https://assets.ubuntu.com/v1/a41aaa61-cklogo-800.png)

Charmed Kubernetes® is pure Kubernetes tested across the widest range of clouds with modern metrics and monitoring, brought to you by the people who deliver Ubuntu.

Google, Microsoft, and many other institutions run Kubernetes on Ubuntu because we focus on the latest container capabilities in modern kernels. That’s why it’s the top choice for enterprise Kubernetes, too.

![](https://assets.ubuntu.com/v1/843c77b6-juju-at-a-glace.svg)

## Deploying Charmed Kubernetes®

To learn more about **Charmed Kubernetes**®, including how to install it on your own cloud, please visit the [Documentation](https://ubuntu.com/kubernetes/docs).

## Contributing to Charmed Kubernetes®

Charmed Kubernetes is an open source project and we welcome contributions of code, additions to the documentation, feature requests and any and all types of
feedback. For more on contributing, see the [official documentation][get-in-touch] on how to contact the team.

## This Juju bundle

This repository contains the code to generate charm bundles used to deploy Charmed Kubernetes, as well as some bundle overlays used to preconfigure certain features
(for example, for running on particular clouds). In general, users will fetch the published bundles from the [Charm Store][], not this repository. If you are working
on the bundle itself, see the [BUILD.md](./BUILD.md) file for more information on building the Charmed Kubernetes bundles.
To contribute to this bundle, see the [CONTRIBUTING.md](./CONTRIBUTING.md) guide.

## container-images.txt

The `container-images.txt` file included in this repository lists the set of containers used by
Charmed-Kubernetes.  Each line in the file represents either a `static` requirement or a `dynamic` requirement. 

The `static` lines reflect a unique set of images required by either the continuous integration tests
against charmed kubernetes `ci-static` or the unique set of images required by a specific release (`v1.21-static`).

The `upstream` lines reflect a unique set of images which are required by a point release of kubernetes
during its rc and release stages (`v1.24.1-upstream`).

The file can be updated manually if the change is simple or can make use of the `images.py` merge tool

```shell
# Usage examples

## Create a new line in the file at v1.25-static from v1.24-static
./images.py copy-from v1.24-static --new_line_id v1.25-static

## Add images to v1.25-static line, merged with existing
./images.py add-to v1.25-static --images gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.18.0 gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.19.0 gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.2.1 gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.20.0 gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.21.1 gcr.io/cloud-provider-vsphere/cpi/release/manager:v1.22.3 gcr.io/cloud-provider-vsphere/csi/release/driver:v2.5.1 gcr.io/cloud-provider-vsphere/csi/release/syncer:v2.5.1 k8s.gcr.io/sig-storage/csi-attacher:v3.4.0 k8s.gcr.io/sig-storage/csi-node-driver-registrar:v2.5.0 k8s.gcr.io/sig-storage/csi-provisioner:v3.1.0 k8s.gcr.io/sig-storage/csi-resizer:v1.4.0 k8s.gcr.io/sig-storage/csi-snapshotter:v5.0.1 k8s.gcr.io/sig-storage/livenessprobe:v2.6.0
```

Note: A guarantee about the contents of this file is that rocks.canonical.com:443 image repository will contain
each image listed in this file in sync with its upstream source at rocks.canonical.com:443/cdk

## Other repositories

The Charmed Kubernetes organisation has a large number of repositories. The majority of these are for specific Juju charms, used to deploy the applications which go to make up Charmed Kubernetes. A few which may be of particular interest:

- The Kubernetes Control Plane charm  - <https://github.com/charmed-kubernetes/charm-kubernetes-master>
- The Kubernetes Worker charm - <https://github.com/charmed-kubernetes/charm-kubernetes-worker>
- The MetalLB operator charm - <https://github.com/charmed-kubernetes/metallb-operator>

Other repositories include:

- The Jenkins scripts used to build and test Charmed Kubernetes - <https://github.com/charmed-kubernetes/jenkins>
- The Charmed Kubernetes documentation - <https://github.com/charmed-kubernetes/kubernetes-docs>
 

<!-- LINKS -->
[Charm Store]: https://jaas.ai/charmed-kubernetes/bundle
[docs]: https://ubuntu.com/kubernetes/docs
[get-in-touch]: https://ubuntu.com/kubernetes/docs/get-in-touch
