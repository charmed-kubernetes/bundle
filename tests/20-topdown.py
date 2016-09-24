#!/usr/bin/python3

import amulet
import os
import subprocess
import time
import unittest
import yaml

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
        print ("=================================")
        cmd = ['tests/attach_local_resources.sh']
        subprocess.check_call(cmd)
        # Wait for the system to settle down.
        cls.deployment.sentry.wait()

        cls.kubemaster = cls.deployment.sentry['kubernetes-master']
        cls.worker = cls.deployment.sentry['kubernetes-worker']
        cls.etcd = cls.deployment.sentry['etcd']
        cls.easyrsa = cls.deployment.sentry['easyrsa']
        cls.loadbalancer = cls.deployment.sentry['kubeapi-load-balancer']

    def test_things(self):
        print('nope')

if __name__ == '__main__':
    unittest.main()
