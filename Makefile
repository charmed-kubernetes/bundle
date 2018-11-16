default: clean
	./bundle k8s/cdk cni/flannel -o ./bundles/cdk-flannel
	./bundle k8s/cdk cni/flannel legacy-storage/ceph -o ./bundles/cdk-flannel-ceph
	./bundle k8s/cdk cni/flannel monitor/graylog -o ./bundles/cdk-flannel-graylog
	./bundle k8s/cdk cni/flannel monitor/prometheus -o ./bundles/cdk-flannel-prometheus
	./bundle k8s/cdk cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-flannel-prometheus-graylog
	./bundle k8s/cdk-aws cni/flannel -o ./bundles/cdk-aws-flannel
	./bundle k8s/cdk-aws cni/flannel monitor/graylog -o ./bundles/cdk-aws-flannel-graylog
	./bundle k8s/cdk-aws cni/flannel monitor/prometheus -o ./bundles/cdk-aws-flannel-prometheus
	./bundle k8s/cdk-aws cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-aws-flannel-prometheus-graylog
	./bundle k8s/cdk-azure cni/flannel -o ./bundles/cdk-azure-flannel
	./bundle k8s/cdk-azure cni/flannel monitor/graylog -o ./bundles/cdk-azure-flannel-graylog
	./bundle k8s/cdk-azure cni/flannel monitor/prometheus -o ./bundles/cdk-azure-flannel-prometheus
	./bundle k8s/cdk-azure cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-azure-flannel-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/flannel -o ./bundles/cdk-baremetal-flannel
	./bundle k8s/cdk-baremetal cni/flannel legacy-storage/ceph -o ./bundles/cdk-baremetal-flannel-ceph
	./bundle k8s/cdk-baremetal cni/flannel monitor/graylog -o ./bundles/cdk-baremetal-flannel-graylog
	./bundle k8s/cdk-baremetal cni/flannel monitor/prometheus -o ./bundles/cdk-baremetal-flannel-prometheus
	./bundle k8s/cdk-baremetal cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-baremetal-flannel-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/flannel monitor/prometheus legacy-storage/ceph -o ./bundles/cdk-baremetal-flannel-prometheus-graylog-ceph
	./bundle k8s/cdk-gcp cni/flannel -o ./bundles/cdk-gcp-flannel
	./bundle k8s/cdk-gcp cni/flannel monitor/graylog -o ./bundles/cdk-gcp-flannel-graylog
	./bundle k8s/cdk-gcp cni/flannel monitor/prometheus -o ./bundles/cdk-gcp-flannel-prometheus
	./bundle k8s/cdk-gcp cni/flannel monitor/prometheus monitor/graylog  -o ./bundles/cdk-gcp-flannel-prometheus-graylog
	./bundle k8s/cdk-openstack cni/flannel -o ./bundles/cdk-openstack-flannel
	./bundle k8s/cdk-openstack cni/flannel monitor/graylog -o ./bundles/cdk-openstack-flannel-graylog
	./bundle k8s/cdk-openstack cni/flannel monitor/prometheus -o ./bundles/cdk-openstack-flannel-prometheus
	./bundle k8s/cdk-openstack cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-openstack-flannel-prometheus-graylog
	./bundle k8s/cdk-vmware cni/flannel -o ./bundles/cdk-vmware-flannel
	./bundle k8s/cdk-vmware cni/flannel legacy-storage/ceph -o ./bundles/cdk-vmware-flannel-ceph
	./bundle k8s/cdk-vmware cni/flannel monitor/graylog -o ./bundles/cdk-vmware-flannel-graylog
	./bundle k8s/cdk-vmware cni/flannel monitor/prometheus -o ./bundles/cdk-vmware-flannel-prometheus
	./bundle k8s/cdk-vmware cni/flannel monitor/prometheus monitor/graylog -o ./bundles/cdk-vmware-flannel-prometheus-graylog
	./bundle k8s/core cni/flannel -o ./bundles/core-flannel
	./bundle k8s/core cni/flannel monitor/graylog -o ./bundles/core-flannel-graylog
	./bundle k8s/core cni/flannel monitor/prometheus -o ./bundles/core-flannel-prometheus
	./bundle k8s/core cni/flannel monitor/prometheus monitor/graylog -o ./bundles/core-flannel-prometheus-graylog
	./bundle k8s/cdk-edge cni/flannel -o ./bundles/cdk-edge-flannel
	./bundle k8s/cdk-edge cni/flannel legacy-storage/ceph -o ./bundles/cdk-edge-flannel-ceph
	./bundle k8s/cdk-edge cni/flannel monitor/graylog legacy-storage/ceph -o ./bundles/cdk-edge-flannel-graylog-ceph
	./bundle k8s/cdk-edge cni/flannel monitor/prometheus legacy-storage/ceph -o ./bundles/cdk-edge-flannel-prometheus-ceph
	./bundle k8s/cdk-edge cni/flannel monitor/prometheus monitor/graylog legacy-storage/ceph -o ./bundles/cdk-edge-flannel-prometheus-graylog-ceph
	./bundle k8s/cdk-aws cni/calico -o ./bundles/cdk-aws-calico
	./bundle k8s/cdk-aws cni/calico monitor/graylog -o ./bundles/cdk-aws-calico-graylog
	./bundle k8s/cdk-aws cni/calico monitor/prometheus -o ./bundles/cdk-aws-calico-prometheus
	./bundle k8s/cdk-aws cni/calico monitor/prometheus monitor/graylog -o ./bundles/cdk-aws-calico-prometheus-graylog
	./bundle k8s/cdk-azure cni/calico -o ./bundles/cdk-azure-calico
	./bundle k8s/cdk-azure cni/calico monitor/graylog -o ./bundles/cdk-azure-calico-graylog
	./bundle k8s/cdk-azure cni/calico monitor/prometheus -o ./bundles/cdk-azure-calico-prometheus
	./bundle k8s/cdk-azure cni/calico monitor/prometheus monitor/graylog -o ./bundles/cdk-azure-calico-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/calico -o ./bundles/cdk-baremetal-calico
	./bundle k8s/cdk-baremetal cni/calico legacy-storage/ceph -o ./bundles/cdk-baremetal-calico-ceph
	./bundle k8s/cdk-baremetal cni/calico monitor/graylog -o ./bundles/cdk-baremetal-calico-graylog
	./bundle k8s/cdk-baremetal cni/calico monitor/prometheus -o ./bundles/cdk-baremetal-calico-prometheus
	./bundle k8s/cdk-baremetal cni/calico monitor/prometheus monitor/graylog -o ./bundles/cdk-baremetal-calico-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/calico monitor/prometheus monitor/graylog legacy-storage/ceph -o ./bundles/cdk-baremetal-calico-prometheus-graylog-ceph
	./bundle k8s/cdk-gcp cni/calico -o ./bundles/cdk-gcp-calico
	./bundle k8s/cdk-gcp cni/calico monitor/graylog -o ./bundles/cdk-gcp-calico-graylog
	./bundle k8s/cdk-gcp cni/calico monitor/prometheus -o ./bundles/cdk-gcp-calico-prometheus
	./bundle k8s/cdk-gcp cni/calico monitor/graylog -o ./bundles/cdk-gcp-calico-prometheus-graylog
	./bundle k8s/cdk-openstack cni/calico -o ./bundles/cdk-openstack-calico
	./bundle k8s/cdk-openstack cni/calico monitor/graylog -o ./bundles/cdk-openstack-calico-graylog
	./bundle k8s/cdk-openstack cni/calico monitor/prometheus -o ./bundles/cdk-openstack-calico-prometheus
	./bundle k8s/cdk-openstack cni/calico monitor/prometheus monitor/graylog -o ./bundles/cdk-openstack-calico-prometheus-graylog
	./bundle k8s/cdk-vmware cni/calico -o ./bundles/cdk-vmware-calico
	./bundle k8s/cdk-vmware cni/calico monitor/graylog -o ./bundles/cdk-vmware-calico-graylog
	./bundle k8s/cdk-vmware cni/calico monitor/prometheus -o ./bundles/cdk-vmware-calico-prometheus
	./bundle k8s/cdk-vmware cni/calico monitor/prometheus monitor/graylog -o ./bundles/cdk-vmware-calico-prometheus-graylog
	./bundle k8s/cdk cni/calico -o ./bundles/cdk-calico
	./bundle k8s/cdk cni/calico legacy-storage/ceph -o ./bundles/cdk-calico-ceph
	./bundle k8s/cdk cni/calico monitor/graylog -o ./bundles/cdk-calico-graylog
	./bundle k8s/cdk cni/calico monitor/prometheus -o ./bundles/cdk-calico-prometheus
	./bundle k8s/cdk cni/calico monitor/graylog monitor/prometheus -o ./bundles/cdk-calico-prometheus-graylog
	./bundle k8s/core cni/calico -o ./bundles/core-calico
	./bundle k8s/core cni/calico monitor/graylog -o ./bundles/core-calico-graylog
	./bundle k8s/core cni/calico monitor/prometheus -o ./bundles/core-calico-prometheus
	./bundle k8s/core cni/calico monitor/graylog monitor/prometheus -o ./bundles/core-calico-prometheus-graylog
	./bundle k8s/cdk-edge cni/calico -o ./bundles/cdk-edge-calico
	./bundle k8s/cdk-edge cni/calico legacy-storage/ceph -o ./bundles/cdk-edge-calico-ceph
	./bundle k8s/cdk-edge cni/calico legacy-storage/ceph monitor/graylog -o ./bundles/cdk-edge-calico-graylog-ceph
	./bundle k8s/cdk-edge cni/calico legacy-storage/ceph monitor/prometheus -o ./bundles/cdk-edge-calico-prometheus-ceph
	./bundle k8s/cdk-edge cni/calico legacy-storage/ceph monitor/graylog monitor/prometheus -o ./bundles/cdk-edge-calico-prometheus-graylog-ceph
	./bundle k8s/cdk cni/canal -o ./bundles/cdk-canal
	./bundle k8s/cdk cni/canal legacy-storage/ceph -o ./bundles/cdk-canal-ceph
	./bundle k8s/cdk cni/canal monitor/graylog -o ./bundles/cdk-canal-graylog
	./bundle k8s/cdk cni/canal monitor/prometheus -o ./bundles/cdk-canal-prometheus
	./bundle k8s/cdk cni/canal monitor/graylog monitor/prometheus -o ./bundles/cdk-canal-prometheus-graylog
	./bundle k8s/cdk-aws cni/canal -o ./bundles/cdk-aws-canal
	./bundle k8s/cdk-aws cni/canal monitor/graylog -o ./bundles/cdk-aws-canal-graylog
	./bundle k8s/cdk-aws cni/canal monitor/prometheus -o ./bundles/cdk-aws-canal-prometheus
	./bundle k8s/cdk-aws cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-aws-canal-prometheus-graylog
	./bundle k8s/cdk-azure cni/canal -o ./bundles/cdk-azure-canal
	./bundle k8s/cdk-azure cni/canal monitor/graylog -o ./bundles/cdk-azure-canal-graylog
	./bundle k8s/cdk-azure cni/canal monitor/prometheus -o ./bundles/cdk-azure-canal-prometheus
	./bundle k8s/cdk-azure cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-azure-canal-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/canal -o ./bundles/cdk-baremetal-canal
	./bundle k8s/cdk-baremetal cni/canal legacy-storage/ceph -o ./bundles/cdk-baremetal-canal-ceph
	./bundle k8s/cdk-baremetal cni/canal monitor/graylog -o ./bundles/cdk-baremetal-canal-graylog
	./bundle k8s/cdk-baremetal cni/canal monitor/prometheus -o ./bundles/cdk-baremetal-canal-prometheus
	./bundle k8s/cdk-baremetal cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-baremetal-canal-prometheus-graylog
	./bundle k8s/cdk-baremetal cni/canal monitor/prometheus monitor/graylog legacy-storage/ceph -o ./bundles/cdk-baremetal-canal-prometheus-graylog-ceph
	./bundle k8s/cdk-gcp cni/canal -o ./bundles/cdk-gcp-canal
	./bundle k8s/cdk-gcp cni/canal monitor/graylog -o ./bundles/cdk-gcp-canal-graylog
	./bundle k8s/cdk-gcp cni/canal monitor/prometheus -o ./bundles/cdk-gcp-canal-prometheus
	./bundle k8s/cdk-gcp cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-gcp-canal-prometheus-graylog
	./bundle k8s/cdk-openstack cni/canal -o ./bundles/cdk-openstack-canal
	./bundle k8s/cdk-openstack cni/canal monitor/graylog -o ./bundles/cdk-openstack-canal-graylog
	./bundle k8s/cdk-openstack cni/canal monitor/prometheus -o ./bundles/cdk-openstack-canal-prometheu
	./bundle k8s/cdk-openstack cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-openstack-canal-prometheus-graylog
	./bundle k8s/cdk-vmware cni/canal -o ./bundles/cdk-vmware-canal
	./bundle k8s/cdk-vmware cni/canal legacy-storage/ceph -o ./bundles/cdk-vmware-canal-ceph
	./bundle k8s/cdk-vmware cni/canal monitor/graylog -o ./bundles/cdk-vmware-canal-graylog
	./bundle k8s/cdk-vmware cni/canal monitor/prometheus -o ./bundles/cdk-vmware-canal-prometheus
	./bundle k8s/cdk-vmware cni/canal monitor/prometheus monitor/graylog -o ./bundles/cdk-vmware-canal-prometheus-graylog
	./bundle k8s/core cni/canal -o ./bundles/core-canal
	./bundle k8s/core cni/canal monitor/graylog -o ./bundles/core-canal-graylog
	./bundle k8s/core cni/canal monitor/graylog monitor/prometheus -o ./bundles/core-canal-prometheus
	./bundle k8s/core cni/canal monitor/graylog monitor/prometheus monitor/graylog -o ./bundles/core-canal-prometheus-graylog
	./bundle k8s/cdk-edge cni/canal -o ./bundles/cdk-edge-canal
	./bundle k8s/cdk-edge cni/canal legacy-storage/ceph -o ./bundles/cdk-edge-canal-ceph
	./bundle k8s/cdk-edge cni/canal legacy-storage/ceph monitor/graylog -o ./bundles/cdk-edge-canal-graylog-ceph
	./bundle k8s/cdk-edge cni/canal legacy-storage/ceph monitor/prometheus -o ./bundles/cdk-edge-canal-prometheus-ceph
	./bundle k8s/cdk-edge cni/canal legacy-storage/ceph monitor/graylog monitor/prometheus -o ./bundles/cdk-edge-canal-prometheus-graylog-ceph
clean:
	rm -rf ./bundles                           
