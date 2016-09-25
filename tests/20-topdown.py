#!/usr/bin/python3

import amulet
import os
import unittest
import yaml

from amulet_utils import (
    check_systemd_service,
    kubectl,
    run,
    valid_certificate,
    valid_key
)

SECONDS_TO_WAIT = 1200


class TestLocalBundle(unittest.TestCase):
    ''' Test Local Bundle tests the top down view of the kubernetes deployment,
        and will perform baseline verification that all deployed
        applications have performed their role in the setup'''

    @classmethod
    def setUpClass(cls):
        """Read the bundle in and deploy the bundle."""
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
        # print("=================================")
        # cmd = ['tests/attach_local_resources.sh']
        # subprocess.check_call(cmd)
        # Wait for the system to settle down.
        cls.deployment.sentry.wait()

        cls.masters = cls.deployment.sentry['kubernetes-master']
        cls.workers = cls.deployment.sentry['kubernetes-worker']
        cls.etcds = cls.deployment.sentry['etcd']
        cls.easyrsas = cls.deployment.sentry['easyrsa']
        cls.loadbalancers = cls.deployment.sentry['kubeapi-load-balancer']

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

# TODO Test creating a small container or pod and delete it.


if __name__ == '__main__':
    unittest.main()
