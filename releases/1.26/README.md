
# Charmed Kubernetes

![](https://img.shields.io/badge/kubernetes-1.26-brightgreen.svg) ![](https://img.shields.io/badge/juju-2.9+-brightgreen.svg)

## Overview

This is a scaled-out Kubernetes cluster composed of the following components and features:

-   Deep integration for public and private clouds, or bare metal
-   Uses standard upstream Kubernetes
-   Multiple Kubernetes control-plane and worker nodes
-   Extensive CNI options
-   Intra-node TLS by default
-   GPGPU support for high performance AI/ML
-   Managed option available

For a more minimal cluster suitable for testing, deploy the smaller
[kubernetes-core](https://charmhub.io/kubernetes-core) bundle.

For a lightweight upstream K8s, try [MicroK8s](https://microk8s.io)!


# Documentation

For detailed instructions on how to deploy and manage **Charmed Kubernetes**, please visit the 
[official Charmed Kubernetes docs](https://www.ubuntu.com/kubernetes/docs/).


# Calico

Calico is used as a CNI plugin to manage networking for the Kubernetes cluster.

## Configuration

**ipip**: Enable IP tunneling. *string, default Never*

**nat-outgoing**: NAT outgoing traffic. *boolean, default true*

**vxlan**: VXLAN encapsulation mode. *string, default Always*

