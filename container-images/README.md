# OCI Images for Charmed Kubernetes

The text files in this directory contain all OCI images that may be required
for a Charmed Kubernetes release.

## Compare release images

Compare images for the `1.19.9` and `1.21.0-rc.0` releases, showing only
images that are new for `1.21.0-rc.0`:
```bash
comm -13 \
  <(curl -s https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/v1.19.9.txt | sort) \
  <(curl -s https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/v1.21.0-rc.0.txt | sort)
```

Output:
```
coredns/coredns:1.8.3
coreos/kube-state-metrics:v1.9.8
defaultbackend-ppc64le:1.5
k8s-artifacts-prod/ingress-nginx/controller:v0.44.0
k8scloudprovider/cinder-csi-plugin:v1.20.0
k8scloudprovider/k8s-keystone-auth:v1.20.0
k8scloudprovider/openstack-cloud-controller-manager:v1.20.0
kubernetesui/dashboard:v2.2.0
kubernetesui/metrics-scraper:v1.0.6
pause:3.4.1
sig-storage/csi-attacher:v2.2.1
sig-storage/csi-node-driver-registrar:v1.3.0
sig-storage/csi-provisioner:v1.6.1
sig-storage/csi-resizer:v0.5.1
sig-storage/csi-snapshotter:v2.1.3
sig-storage/livenessprobe:v2.1.0
```

Compare all images for the `1.19.9` and `1.21.0-rc.0` releases:
```bash
comm \
  <(curl -s https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/v1.19.9.txt | sort) \
  <(curl -s https://raw.githubusercontent.com/charmed-kubernetes/bundle/master/container-images/v1.21.0-rc.0.txt | sort)
```

The output shows `1.19.9` images in the first column, `1.21.0-rc.0` images in
the second colum, and images common to both releases in the third column:
```
		cdkbot/microbot-amd64:latest
		cdkbot/microbot-arm64:latest
		cdkbot/microbot-s390x:latest
		cdkbot/registry-amd64:2.6
		cdkbot/registry-arm64:2.6
		cephcsi/cephcsi:v2.1.2
coredns/coredns:1.6.7
	coredns/coredns:1.8.3
coreos/kube-state-metrics:v1.9.7
	coreos/kube-state-metrics:v1.9.8
		defaultbackend-amd64:1.5
		defaultbackend-arm64:1.5
	defaultbackend-ppc64le:1.5
		defaultbackend-s390x:1.4
		external_storage/nfs-client-provisioner:v3.1.0-k8s1.11
k8s-artifacts-prod/ingress-nginx/controller:v0.34.1
	k8s-artifacts-prod/ingress-nginx/controller:v0.44.0
k8scloudprovider/cinder-csi-plugin:v1.18.0
	k8scloudprovider/cinder-csi-plugin:v1.20.0
k8scloudprovider/k8s-keystone-auth:v1.19.0
	k8scloudprovider/k8s-keystone-auth:v1.20.0
k8scloudprovider/openstack-cloud-controller-manager:v1.18.0
	k8scloudprovider/openstack-cloud-controller-manager:v1.20.0
		k8scsi/csi-attacher:v2.1.1
k8scsi/csi-node-driver-registrar:v1.2.0
		k8scsi/csi-node-driver-registrar:v1.3.0
		k8scsi/csi-provisioner:v1.4.0
k8scsi/csi-resizer:v0.4.0
		k8scsi/csi-resizer:v0.5.0
		k8scsi/csi-snapshotter:v1.2.2
		k8s-dns-dnsmasq-nanny:1.15.10
		k8s-dns-kube-dns:1.15.10
		k8s-dns-sidecar:1.15.10
		kubernetes-ingress-controller/nginx-ingress-controller-ppc64le:0.20.0
kubernetesui/dashboard:v2.0.1
	kubernetesui/dashboard:v2.2.0
kubernetesui/metrics-scraper:v1.0.4
	kubernetesui/metrics-scraper:v1.0.6
		metrics-server-amd64:v0.3.6
		metrics-server-arm64:v0.3.6
		metrics-server-ppc64le:v0.3.6
		metrics-server-s390x:v0.3.6
		nvidia/k8s-device-plugin:v0.9.0
pause:3.2
	pause:3.4.1
		rancher/rancher:latest
	sig-storage/csi-attacher:v2.2.1
	sig-storage/csi-node-driver-registrar:v1.3.0
	sig-storage/csi-provisioner:v1.6.1
	sig-storage/csi-resizer:v0.5.1
	sig-storage/csi-snapshotter:v2.1.3
	sig-storage/livenessprobe:v2.1.0
		sonatype/nexus3:latest
```
