
default: clean
	./bundle k8s/cdk cni/flannel -o ..
	./bundle k8s/cdk cni/flannel monitor/elastic -o ../bundles/cdk-flannel-elastic
	./bundle k8s/core cni/flannel -o ../bundles/core-flannel
	./bundle k8s/core cni/flannel monitor/elastic -o ../bundles/core-flannel-elastic

clean:
	rm -rf ../bundle.yaml
	rm -rf ../README.md
	rm -rf ../bundles
