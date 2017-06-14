#!/usr/bin/python3

import amulet
import os
import unittest
import yaml

from amulet_utils import check_systemd_service
from amulet_utils import kubectl
from amulet_utils import run

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
        cls.deployment = amulet.Deployment(series='xenial')
        with open(cls.bundle_file) as stream:
            bundle_yaml = stream.read()
        bundle = yaml.safe_load(bundle_yaml)
        cls.deployment.load(bundle)

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)

        # Wait for the system to settle down.
        application_messages = {'kubernetes-worker':
                                'Kubernetes worker running.'}
        cls.deployment.sentry.wait_for_messages(application_messages,
                                                timeout=900)

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

    def test_kubeconfig_presence(self):
        '''Test that the kubeconfig exists so that kubectl commands can run.'''
        # typical client configs
        for master in self.masters:
            output, rc = master.run('grep server: /home/ubuntu/config')
            self.assertTrue(rc == 0)

        # typical client configs
        for worker in self.workers:
            ubuntu, rc = worker.run('grep server: /home/ubuntu/.kube/config')
            self.assertTrue(rc == 0)
            root, rc = worker.run('grep server: /root/.kube/config')
            self.assertTrue(rc == 0)
            self.assertTrue(ubuntu == root)

        # post rbac component configs
        for worker in self.workers:
            kubelet, rc = worker.run('grep token: /root/cdk/kubeletconfig')
            self.assertTrue(rc == 0)
            proxy, rc = worker.run('grep token: /root/cdk/kubeproxyconfig')
            self.assertTrue(rc == 0)
            self.assertTrue(kubelet != proxy)


    def test_kubeconfig_contents(self):
        '''Validate the contents of the client config has no client keys.'''

        for master in self.masters:
            config = master.file_contents('/home/ubuntu/config')
            cfg_dict = yaml.safe_load(config)
            user_keys = cfg_dict['users'][0]['user'].keys()
            self.assertTrue('token' in user_keys)
            self.assertTrue('client_key' not in user_keys)
            self.assertTrue('client_cert' not in user_keys)


    def test_kube_system_sa(self):
        ''' Validate the kube-system service accounts exist '''
        cmd = "/snap/bin/kubectl get sa --namespace=kube-system"
        for master in self.masters:
            val, rc = master.run(cmd)
            self.assertTrue('kube-dns' in val)
            self.assertTrue('default' in val)
            self.assertTrue(rc == 0)

        # validate that we have a cluster role binding for the addon manager
        crbcmd = '/snap/bin/kubectl get clusterrolebindings'
        val, rc = self.masters[0].run(crbcmd)
        self.assertTrue('add-on-cluster-admin' in val)
        self.assertTrue(rc == 0)

    def test_kube_worker_tokens(self):
        ''' Read that every kubelet config and proxy config has a static token
        for authentication '''
        tokens = self.masters[0].file_contents('/root/cdk/known_tokens.csv')
        for worker in self.workers:
            self.assertTrue(worker.info['unit_name'] in tokens)
            kubelet = worker.file_contents('/root/cdk/kubeletconfig')
            proxy = worker.file_contents('/root/cdk/kubeproxyconfig')
            self.assertTrue('token:' in kubelet)
            self.assertTrue('token:' in proxy)

    def test_master_apiserver_args(self):
        ''' Validate the master no longer has a client cert in args '''
        for master in self.masters:
            argf = '/var/snap/kube-apiserver/current/args'
            args = master.file_contents(argf)

            self.assertFalse('--client-certificate' in args)
            self.assertTrue('--basic-auth-file' in args)
            self.assertTrue('--token-auth-file' in args)
            self.assertTrue('/root/cdk/known_tokens.csv' in args)
            self.assertTrue('/root/cdk/basic_auth.csv' in args)


if __name__ == '__main__':
    unittest.main()
