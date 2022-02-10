#!/usr/bin/python3

from amulet_utils import wait

import amulet
import os
import unittest
import yaml
import requests
import time
import random
import string


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

        # Make every unit available through self reference
        # eg: for worker in self.workers:
        #         print(worker.info['public-address'])
        cls.easyrsas = cls.deployment.sentry['easyrsa']
        cls.etcds = cls.deployment.sentry['etcd']
        cls.flannels = cls.deployment.sentry['flannel']
        cls.loadbalancers = cls.deployment.sentry['kubeapi-load-balancer']
        cls.masters = cls.deployment.sentry['kubernetes-master']
        cls.workers = cls.deployment.sentry['kubernetes-worker']

    def test_unauthenticated(self):
        '''Test if the master services are accessible without credentials.'''
        url = 'https://{}:443/'.format(self.loadbalancers[0].info['public-address'])
        r = requests.get(url, verify=False)
        self.assertEqual(r.status_code, 401)

    def test_basic(self):
        '''Test the effect of changing the admin password'''
        ip = self.loadbalancers[0].info['public-address']
        # Try wrong password
        status = self.get_ui(ip, 'wrongpassword')
        self.assertEqual(status, 401)
        # Get current password
        password = self.get_password()
        self.assertNotEqual(password, 'admin')
        t0 = time.time()
        while time.time() - t0 < 600:
            status = self.get_ui(ip, password)
            if status == 200:
                break
            time.sleep(1)
        self.assertEqual(status, 200)
        # Change password
        alpha = string.ascii_letters + string.digits
        new_password = ''.join(random.SystemRandom().choice(alpha) for _ in range(8))
        self.deployment.configure('kubernetes-master',
                                  {
                                      'client_password': new_password,
                                  })
        time.sleep(20)  # give a chance for reactive to run
        self.deployment.sentry.wait()
        status = self.get_ui(ip, password)
        self.assertEqual(status, 401)
        status = self.get_ui(ip, new_password)
        self.assertEqual(status, 200)

    def get_ui(self, ip_addr, password, user='admin'):
        """Access the dashboard URL.

        The URL changes based on the k8s version. Check snap info on the
        sentried k8s-master to use the appropriate url.
        """
        # snap info for kube-apiserver looks like this:
        #   tracking:                1.10/edge
        cmd = "snap info kube-apiserver | grep tracking"
        output, rc = self.masters[0].run(cmd)
        version = output.split()[1]
        if version.startswith('1.7'):
            url_path = "/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy/"
        else:
            url_path = "/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/"

        url = "https://{}:443{}".format(ip_addr, url_path)
        print("Requesting dashboard from: {}".format(url))
        r = requests.get(url, auth=requests.auth.HTTPBasicAuth(user, password),
                         verify=False)
        return r.status_code

    def get_password(self):
        content = self.masters[0].file_contents('/home/ubuntu/config')
        config = yaml.safe_load(content)
        return config['users'][0]['user']['password']


if __name__ == '__main__':
    unittest.main()
