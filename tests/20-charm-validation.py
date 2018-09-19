#!/usr/bin/python3

import amulet
import os
import unittest
import yaml
import uuid
import time

from amulet_utils import check_systemd_service
from amulet_utils import kubectl
from amulet_utils import run
from amulet_utils import valid_certificate
from amulet_utils import valid_key
from amulet_utils import wait

SECONDS_TO_WAIT = 1800


def find_bundle(name='bundle.yaml'):
    '''Locate the bundle to load for this test.'''
    # Check the environment variables for BUNDLE.
    bundle_path = os.getenv('BUNDLE_PATH')
    if not bundle_path:
        # Construct bundle path from the location of this file.
        bundle_path = os.path.join(os.path.dirname(__file__), '..', name)
    return bundle_path


class IntegrationTest(unittest.TestCase):
    bundle_file = find_bundle()

    @classmethod
    def setUpClass(cls):
        cls.deployment = amulet.Deployment(series='bionic')
        with open(cls.bundle_file) as stream:
            bundle_yaml = stream.read()
        bundle = yaml.safe_load(bundle_yaml)
        cls.deployment.load(bundle)

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)

        # Wait for the system to settle down.
        wait(cls.deployment.sentry)

    @property
    def easyrsas(self):
        return self.deployment.sentry['easyrsa']

    @property
    def etcds(self):
        return self.deployment.sentry['etcd']

    @property
    def flannels(self):
        return self.deployment.sentry['flannel']

    @property
    def loadbalancers(self):
        return self.deployment.sentry['kubeapi-load-balancer']

    @property
    def masters(self):
        return self.deployment.sentry['kubernetes-master']

    @property
    def workers(self):
        return self.deployment.sentry['kubernetes-worker']

    def test_master_services(self):
        '''Test if the master services are running.'''
        for master in self.masters:
            services = [
                'snap.kube-apiserver.daemon',
                'snap.kube-controller-manager.daemon',
                'snap.kube-scheduler.daemon'
            ]
            for service in services:
                self.assertTrue(check_systemd_service(master, service))

    def test_worker_services(self):
        '''Test if the worker services are running.'''
        for worker in self.workers:
            services = [
                'docker',
                'snap.kubelet.daemon',
                'snap.kube-proxy.daemon'
            ]
            for service in services:
                self.assertTrue(check_systemd_service(worker, service))

    def test_tls(self):
        '''Test that the master and worker nodes have the right tls files.'''
        for master in self.masters:
            # There should be three certificates on each master node.
            crts = [
                '/root/cdk/ca.crt',
                '/root/cdk/client.crt',
                '/root/cdk/server.crt'
            ]
            for certificate in crts:
                self.assertTrue(valid_certificate(master, certificate))
            # There should be two keys on each master node.
            keys = ['/root/cdk/client.key', '/root/cdk/server.key']
            for key in keys:
                self.assertTrue(valid_key(master, key))
        for worker in self.workers:
            # There should be two certificates on each worker node.
            crts = ['/root/cdk/ca.crt', '/root/cdk/client.crt']
            for certificate in crts:
                self.assertTrue(valid_certificate(worker, certificate))
            # There is only one client key on the worker node.
            client_key = '/root/cdk/client.key'
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
            self.assertTrue(ubuntu == root)

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

    def test_labels(self):
        '''Test labels can be set.'''
        nodes_describe_cmd = kubectl('describe no')
        new_label = str(uuid.uuid4())
        self.deployment.configure('kubernetes-worker', {
            'labels': 'mylabel={}'.format(new_label),
        })
        self.deployment.sentry.wait()
        output, rc = run(self.masters[0], nodes_describe_cmd)
        print("Output {}".format(output))
        self.assertTrue(rc == 0)
        self.assertTrue(new_label in output)

    def test_etcd_scale_on_master(self):
        ''' Scale the etcd units and verify that the apiserver configuration
        has updated to reflect the current scale of etcd '''

        # ensure we aren't running with only 1 etcd unit... k8s core...
        if len(self.etcds) <= 1:
            self.deployment.add_unit('etcd', timeout=1200)
            self.deployment.sentry.wait()

        # Cache the contents of the file before we adjust the scale
        args = '/var/snap/kube-apiserver/current/args'
        api_conf = self.masters[0].file_contents(args)

        # iterate through the file and copy out the apiserver line
        orig_apiserver = ''
        for line in api_conf.split('\n'):
            if '--etcd-servers' in line:
                orig_apiserver = line

        self.assertNotEqual(orig_apiserver, '')

        # discover the leader
        for unit in self.etcds:
            leader_result = unit.run('is-leader')
            if leader_result[0] == 'True':
                leader = unit

        # Now remove an etcd unit (in this case, the leader)
        self.deployment.remove_unit(leader.info['unit_name'])
        self.deployment.sentry.wait(timeout=900)

        # Probe the arg file for all etcd members.
        scaled_api_conf = self.masters[0].file_contents(args)

        # iterate through the file and find the etcdservers
        scaled_apiserver = ''
        for line in scaled_api_conf.split('\n'):
            if '--etcd-servers' in line:
                scaled_apiserver = line

        self.assertNotEqual(scaled_apiserver, '')

        # determine we have the same number of servers as defined in the
        # topology
        server_string = scaled_apiserver.split(" ")[-1]
        split_servers = server_string.split(",")

        self.assertEqual(len(split_servers), len(self.etcds))
        # determine that the actual etcd server string has changed to reflect
        # the number of etcd units in the apiserver connection string.
        self.assertNotEqual(scaled_apiserver, orig_apiserver)

    def test_service_restart(self):
        """
        Trigger service restart action on master

        """
        action_id = self.masters[0].run_action('restart')
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        self.assertEqual(outcome['status'], 'completed')

    def test_namespace_actions(self):
        """
        Test namespace CRUD operations

        """
        action_id = self.masters[0].run_action('namespace-create',
                                               {'name': 'testns'})
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        self.assertEqual(outcome['status'], 'completed')
        action_id = self.masters[0].run_action('namespace-list')
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        self.assertTrue('testns' in outcome['results']['namespaces'])
        action_id = self.masters[0].run_action('namespace-delete',
                                               {'name': 'testns'})
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        self.assertEqual(outcome['status'], 'completed')
        # Allow for kubernetes to remove the namespace
        time.sleep(30)
        action_id = self.masters[0].run_action('namespace-list')
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        self.assertTrue('testns' not in outcome['results']['namespaces'])


if __name__ == '__main__':
    unittest.main()
