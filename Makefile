
default: clean
	./bundle k8s/cdk cni/flannel
	./bundle k8s/cdk cni/flannel monitor/elastic
	./bundle k8s/core cni/flannel
	./bundle k8s/core cni/flannel monitor/elastic
	mkdir bundles
	mv bundle-cdk-flannel bundles
	mv bundle-cdk-flannel-elastic bundles
	mv bundle-core-flannel bundles
	mv bundle-core-flannel-elastic bundles
	cp bundles/bundle-cdk-flannel/* bundles

clean:
	rm -rf bundles
