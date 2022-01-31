# Kubernetes Core Bundle

![](https://img.shields.io/badge/kubernetes-1.23-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.0+-brightgreen.svg)

## Overview

This is a minimal Kubernetes cluster composed of the following components and features:

- Kubernetes (automated deployment, operations, and scaling)
     - Kubernetes cluster with one control-plane node and one worker node.
     - TLS used for communication between nodes for security.
     - A CNI plugin (Flannel)
     - Optional Ingress Controller (on worker)
     - Optional Dashboard addon (on control-plane) including Heapster for cluster monitoring
- EasyRSA
     - Performs the role of a certificate authority serving self-signed certificates
       to the requesting units of the cluster.
- Etcd (distributed key value store)
     - One node for basic functionality.

This bundle is suitable for development and testing purposes. For a more robust, scaled-out cluster, deploy the
[charmed-kubernetes](https://charmhub.io/charmed-kubernetes) bundle.

For detailed installation and usage, please see the [Charmed Kubernetes documentation](https://ubuntu.com/kubernetes/docs).

