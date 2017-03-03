#!/usr/bin/python3
import os
import amulet
import unittest
import yaml


SECONDS_TO_WAIT = 1800


class E2eIntegrationTest(unittest.TestCase):
    bundle_file = os.path.join(os.path.dirname(__file__), '..', 'bundle.yaml')

    @classmethod
    def setUpClass(cls):
        cls.deployment = amulet.Deployment()
        with open(cls.bundle_file) as f:
            bun = f.read()
        bundle = yaml.safe_load(bun)
        cls.deployment.load(bundle)
        cls.deployment.add('kubernetes-e2e',
                           charm='~containers/kubernetes-e2e',
                           series='xenial')
        # Editors Note:  Instead of declaring the bundle in the amulet
        # setup stanza, rely on bundletester to deploy the bundle on
        # this tests behalf.  When coupled with reset:false in
        # tests.yaml this yields faster test runs per bundle.

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)
        cls.deployment.relate('kubernetes-e2e:certificates',
                              'easyrsa:client')
        cls.deployment.relate('kubernetes-e2e:kubernetes-master',
                              'kubernetes-master:kube-api-endpoint')
        # Wait for the system to settle down.
        application_messages = {'kubernetes-worker':
                                'Kubernetes worker running.',
                                'kubernetes-e2e':
                                'Ready to test.'}
        cls.deployment.sentry.wait_for_messages(application_messages,
                                                timeout=1800)

        cls.e2e = cls.deployment.sentry['kubernetes-e2e'][0]

    @classmethod
    def tearDownClass(cls):
        cls.deployment.unrelate('kubernetes-e2e:certificates',
                                'easyrsa:client')
        cls.deployment.unrelate('kubernetes-e2e:kubernetes-master',
                                'kubernetes-master:kube-api-endpoint')

    def test_e2e(self):
        '''Trigger e2e tests'''
        args = {'skip': '\[(Flaky|Slow|Feature:.*)\]'}
        action_id = self.e2e.run_action('test', args)
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True )
        self.assertIn('completed', outcome)


if __name__ == '__main__':
    unittest.main()
