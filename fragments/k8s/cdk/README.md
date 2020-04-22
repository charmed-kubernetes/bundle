# The Charmed Distribution of Kubernetes

![](https://img.shields.io/badge/kubernetes-1.19-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.0+-brightgreen.svg)

## Overview

This is a scaled-out Kubernetes cluster composed of the following components and features:

- Multiple Kubernetes master and worker nodes
- Load balancer for master nodes
- Multi-node etcd cluster
- Intra-node TLS by default
- Flannel CNI plugin
- Ingress controller
- Dashboard addon with Heapster for metrics

For a more minimal cluster suitable for development and testing, deploy the smaller
[kubernetes-core](https://jujucharms.com/kubernetes-core) bundle.

# Documentation

For detailed instructions on how to deploy and manage **Charmed Kubernetes**, please visit the 
[official Charmed Kubernetes docs](https://www.ubuntu.com/kubernetes/docs/).

