#!/usr/bin/python3

import amulet
import os
import unittest
import yaml
import requests

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


class ShuffleTest(unittest.TestCase):
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

    def test_scale_master_and_worker_termination(self):
        '''Test we can scale kubernetes masters, and terminate
        workers without errors.'''
        # Ensure we can drop masters
        for master in self.masters:
            self.deployment.remove_unit(master.info['unit_name'])
        self.deployment.sentry.wait(timeout=SECONDS_TO_WAIT)
        assert len(self.masters) is 0

        # Ensure we can have more than one master
        self.deployment.add_unit('kubernetes-master', 2)
        self.deployment.sentry.wait(timeout=SECONDS_TO_WAIT)
        lb_ip = self.loadbalancers[0].info['public-address']
        for master in self.masters:
            output, rc = master.run('grep server: /home/ubuntu/config')
            self.assertTrue(lb_ip in output)
            self.assertTrue(rc == 0)

        # Check that the LB can still reach the masters
        url = 'https://{}:443/ui/'.format(lb_ip)
        r = requests.get(url, verify=False)
        # UI is protected via basic auth so we should get a 401
        # In case the LB was not pointing to the masters we were to get
        # a connection timeout.
        self.assertTrue(r.status_code == 401)


if __name__ == '__main__':
    unittest.main()
