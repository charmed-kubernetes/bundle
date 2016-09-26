#!/usr/bin/python3

import amulet
import os
import unittest
import yaml

from amulet_utils import attach_resource
from amulet_utils import check_systemd_service
from amulet_utils import kubectl
from amulet_utils import run
from amulet_utils import valid_certificate
from amulet_utils import valid_key

SECONDS_TO_WAIT = 1200


class IntegrationTest(unittest.TestCase):
    ''' Test Local Bundle tests the top down view of the kubernetes deployment,
        and will perform baseline verification that all deployed
        applications have performed their role in the setup'''

    @classmethod
    def setUpClass(cls):
        # Get the relative bundle path from the environment variable.
        cls.bundle = os.getenv('BUNDLE', 'local.yaml')
        # Create a path to the bundle based on this file's location.
        cls.bundle_path = os.path.join(cls.bundle)
        # Normalize the path to the bundle.
        cls.bundle_path = os.path.abspath(cls.bundle_path)

        print('Deploying bundle: {0}'.format(cls.bundle_path))
        cls.deployment = amulet.Deployment()
        with open(cls.bundle_path, 'r') as bundle_file:
            contents = yaml.safe_load(bundle_file)
            cls.deployment.load(contents)

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)
        # Attach local resources to charms
        res_path = '/home/ubuntu/resources/{}'
        attach_resource('easyrsa', 'easyrsa',
                        res_path.format('EasyRSA-3.0.1.tgz'))
        attach_resource('flannel', 'flannel',
                        res_path.format('flannel-v0.6.1-amd64.tar.gz'))
        attach_resource('kubernetes-master', 'kubernetes',
                        res_path.format('kubernetes-master.tar.gz'))
        attach_resource('kubernetes-worker', 'kubernetes',
                        res_path.format('kubernetes-worker.tar.gz'))

        # Wait for the system to settle down.
        cls.deployment.sentry.wait()

        # Make every unit available through self reference
        # eg: for worker in self.workers:
        #         print(worker.info['public-address'])
        cls.easyrsas = cls.deployment.sentry['easyrsa']
        cls.etcds = cls.deployment.sentry['etcd']
        cls.flannels = cls.deployment.sentry['flannel']
        cls.loadbalancers = cls.deployment.sentry['kubeapi-load-balancer']
        cls.masters = cls.deployment.sentry['kubernetes-master']
        cls.workers = cls.deployment.sentry['kubernetes-worker']

    def test_master_services(self):
        '''Test if the master services are running.'''
        for master in self.masters:
            services = [
                'kube-apiserver',
                'kube-controller-manager',
                'kube-scheduler'
            ]
            for service in services:
                self.assertTrue(check_systemd_service(master, service))

    def test_worker_services(self):
        '''Test if the worker services are running.'''
        for worker in self.workers:
            services = [
                'docker',
                'kubelet',
                'kube-proxy'
            ]
            for service in services:
                self.assertTrue(check_systemd_service(worker, service))

    def test_tls(self):
        '''Test that the master and worker nodes have the right tls files.'''
        for master in self.masters:
            # There should be three certificates on each master node.
            crts = [
                '/srv/kubernetes/ca.crt',
                '/srv/kubernetes/client.crt',
                '/srv/kubernetes/server.crt'
            ]
            for certificate in crts:
                self.assertTrue(valid_certificate(master, certificate))
            # There should be two keys on each master node.
            keys = ['/srv/kubernetes/client.key', '/srv/kubernetes/server.key']
            for key in keys:
                self.assertTrue(valid_key(master, key))
        for worker in self.workers:
            # There should be two certificates on each worker node.
            crts = ['/srv/kubernetes/ca.crt', '/srv/kubernetes/client.crt']
            for certificate in crts:
                self.assertTrue(valid_certificate(worker, certificate))
            # There is only one client key on the worker node.
            client_key = '/srv/kubernetes/client.key'
            self.assertTrue(valid_key(worker, client_key))

    def test_kubeconfig(self):
        '''Test that the kubeconfig exists so that kubectl commands can run.'''
        for master in self.masters:
            output, rc = master.run('grep server: /home/ubuntu/config')
            self.assertTrue(rc == 0)

        for worker in self.workers:
            ubuntu, rc = worker.run('grep server: /home/ubuntu/.kube/config')
            self.assertTrue(rc == 0)
            root, rc = worker.run('grep server: /root/.kube/config')
            self.assertTrue(rc == 0)
            kubelet, rc = worker.run('grep server: /srv/kubernetes/config')
            self.assertTrue(rc == 0)
            self.assertTrue(ubuntu == root and root == kubelet)

    def test_cluster_info(self):
        '''Test that kubectl is installed and the cluster appears healthy.'''
        for master in self.masters:
            cluster_info = kubectl('cluster-info')
            output, rc = run(master, cluster_info)
            self.assertTrue(rc == 0)
            self.assertTrue('Kubernetes master' in output)
            # TODO Figure out how to wait for KubeDNS before running this test.
            # DNS turnup takes quite a while after the cluster settles.
            # Do not fail when the cluster is still converging on KubeDNS.
            # self.assertTrue('KubeDNS is running' in output)

    def test_kube_pods(self):
        '''Test that the kube-system listing contains the kube-dns pod.'''
        # $ kubectl get pods --namespace=kube-system
        # NAME                                    READY     STATUS    RESTARTS   AGE  # noqa
        # kube-dns-v19-0gpcl                      3/3       Running   0          7m  # noqa
        # kubernetes-dashboard-1655269645-gpfdf   1/1       Running   0          7m  # noqa
        if len(self.masters) > 0:
            unit = self.masters[0]
            get_pods = kubectl('get pods', namespace='kube-system')
            output, rc = run(unit, get_pods)
            self.assertTrue(rc == 0)
            self.assertTrue('kube-dns' in output)

    def test_etcd_binary_placement(self):
        ''' Ensure the etcd binary is placed on the host'''
        for etcd in self.etcds:
            etcdstat = etcd.file_stat('/usr/local/bin/etcd')
            assert etcdstat['size'] > 0
            etcdctlstat = etcd.file_stat('/usr/local/bin/etcdctl')
            assert etcdctlstat['size'] > 0

    def test_flannel_binary_placement(self):
        ''' Ensure the flannel binary is placed on the host'''
        for flannel in self.flannels:
            stat = flannel.file_stat('/usr/local/bin/flanneld')
            assert stat['size'] > 0

    def test_flannel_environment_file(self):
        ''' Ensure the flannel environment file exists'''

        # FLANNEL_NETWORK=10.1.0.0/16
        # FLANNEL_SUBNET=10.1.90.1/24
        # FLANNEL_MTU=1410
        # FLANNEL_IPMASQ=false

        for flannel in self.flannels:
            cont = flannel.file_contents('/var/run/flannel/subnet.env')
            assert 'FLANNEL_NETWORK' in cont
            assert 'FLANNEL_SUBNET' in cont
            assert 'FLANNEL_MTU' in cont
            assert 'FLANNEL_IPMASQ' in cont


# TODO Test creating a small container or pod and delete it.


if __name__ == '__main__':
    unittest.main()
