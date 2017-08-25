# Canal

> Note: this is still in an experimental state. Use at your own risk.

Canal (Calico + Flannel) is used as a CNI plugin to manage networking for the
Kubernetes cluster.

## Configuration

**iface** The interface to configure the flannel SDN binding. If this value is
empty string or undefined the code will attempt to find the default network
adapter similar to the following command:  
```bash
route | grep default | head -n 1 | awk {'print $8'}
```

**cidr** The network range to configure the flannel SDN to declare when
establishing networking setup with etcd. Ensure this network range is not active
on the vlan you're deploying to, as it will cause collisions and odd behavior
if care is not taken when selecting a good CIDR range to assign to flannel.

## Further information

- [Canal Charm Layer](https://github.com/juju-solutions/layer-canal)
- [Canal Project Page](https://github.com/projectcalico/canal)
