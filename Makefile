default: clean
	./bundle k8s/cdk cni/flannel -o ./bundles/cdk-flannel
	./bundle k8s/cdk cni/flannel legacy-storage/ceph -o ./bundles/cdk-flannel-ceph
	./bundle k8s/cdk cni/flannel monitor/elastic -o ./bundles/cdk-flannel-elastic
	./bundle k8s/core cni/flannel -o ./bundles/core-flannel
	./bundle k8s/core cni/flannel monitor/elastic -o ./bundles/core-flannel-elastic
	./bundle k8s/cdk-converged cni/flannel -o ./bundles/cdk-converged-flannel
	./bundle k8s/cdk-converged cni/flannel legacy-storage/ceph -o ./bundles/cdk-converged-flannel-ceph
	./bundle k8s/cdk cni/calico -o ./bundles/cdk-calico
	./bundle k8s/cdk cni/calico legacy-storage/ceph -o ./bundles/cdk-calico-ceph
	./bundle k8s/cdk cni/calico monitor/elastic -o ./bundles/cdk-calico-elastic
	./bundle k8s/core cni/calico -o ./bundles/core-calico
	./bundle k8s/core cni/calico monitor/elastic -o ./bundles/core-calico-elastic
	./bundle k8s/cdk-converged cni/calico -o ./bundles/cdk-converged-calico
	./bundle k8s/cdk-converged cni/calico legacy-storage/ceph -o ./bundles/cdk-converged-calico-ceph
	./bundle k8s/cdk cni/canal -o ./bundles/cdk-canal
	./bundle k8s/cdk cni/canal legacy-storage/ceph -o ./bundles/cdk-canal-ceph
	./bundle k8s/cdk cni/canal monitor/elastic -o ./bundles/cdk-canal-elastic
	./bundle k8s/core cni/canal -o ./bundles/core-canal
	./bundle k8s/core cni/canal monitor/elastic -o ./bundles/core-canal-elastic
	./bundle k8s/cdk-converged cni/canal -o ./bundles/cdk-converged-canal
	./bundle k8s/cdk-converged cni/canal legacy-storage/ceph -o ./bundles/cdk-converged-canal-ceph
	./bundle k8s/cdk cni/cilium -o ./bundles/cdk-cilium
	./bundle k8s/cdk cni/cilium legacy-storage/ceph -o ./bundles/cdk-cilium-ceph
	./bundle k8s/cdk cni/cilium monitor/elastic -o ./bundles/cdk-cilium-elastic
	./bundle k8s/core cni/cilium -o ./bundles/core-cilium
	./bundle k8s/core cni/cilium monitor/elastic -o ./bundles/core-cilium-elastic
	./bundle k8s/cdk-converged cni/cilium -o ./bundles/cdk-converged-cilium
	./bundle k8s/cdk-converged cni/cilium legacy-storage/ceph -o ./bundles/cdk-converged-cilium-ceph


clean:
	rm -rf ./bundles
