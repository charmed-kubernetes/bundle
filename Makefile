
default: clean
	./bundle k8s/cdk cni/flannel -o ../bundles/cdk-flannel
	./bundle k8s/cdk cni/flannel monitor/elastic -o ../bundles/cdk-flannel-elastic
	./bundle k8s/core cni/flannel -o ../bundles/core-flannel
	./bundle k8s/core cni/flannel monitor/elastic -o ../bundles/core-flannel-elastic
	./bundle k8s/cdk cni/calico -o ../bundles/cdk-calico
	./bundle k8s/cdk cni/calico monitor/elastic -o ../bundles/cdk-calico-elastic
	./bundle k8s/core cni/calico -o ../bundles/core-calico
	./bundle k8s/core cni/calico monitor/elastic -o ../bundles/core-calico-elastic

clean:
	rm -rf ../bundle.yaml
	rm -rf ../README.md
	rm -rf ../bundles
