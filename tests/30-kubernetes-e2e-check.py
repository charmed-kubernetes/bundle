#!/usr/bin/python3
import os
import amulet
import unittest
import yaml
import subprocess


SECONDS_TO_WAIT = 1800


class E2eIntegrationTest(unittest.TestCase):
    bundle_file = os.path.join(os.path.dirname(__file__), '..', 'bundle.yaml')

    @classmethod
    def setUpClass(cls):
        """
        Load the bundle and augment it with the latest kubernetes-e2e.

        """
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
        # Allow privileged containers
        cls.deployment.configure('kubernetes-master', {
            'allow-privileged': 'true',
        })
        cls.deployment.configure('kubernetes-worker', {
            'allow-privileged': 'true',
        })
        # Wait for the system to settle down.
        application_messages = {'kubernetes-worker':
                                'Kubernetes worker running.',
                                'kubernetes-e2e':
                                'Ready to test.'}
        cls.deployment.sentry.wait_for_messages(application_messages,
                                                timeout=SECONDS_TO_WAIT)

        cls.e2e = cls.deployment.sentry['kubernetes-e2e'][0]

    @classmethod
    def tearDownClass(cls):
        """
        Removing only the relations to kubernetes-e2e so
        we can re-run the test with out having it complaining
        that these relations already exist.
        """
        cls.deployment.unrelate('kubernetes-e2e:certificates',
                                'easyrsa:client')
        cls.deployment.unrelate('kubernetes-e2e:kubernetes-master',
                                'kubernetes-master:kube-api-endpoint')

    def test_e2e(self):
        """
        Trigger e2e tests and assert the job completed,
        implying successful testing.

        """
        action_id = self.e2e.run_action('test')
        outcome = self.deployment.action_fetch(action_id,
                                               timeout=7200,
                                               raise_on_timeout=True,
                                               full_output=True)
        if 'TEST_RESULT_DIR' in os.environ:
            unit = self.e2e.info['unit_name']
            test_result_dir = os.environ['TEST_RESULT_DIR']
            for suffix in ['.log.tar.gz', '-junit.tar.gz']:
                src = '%s:%s%s' % (unit, action_id, suffix)
                dest = os.path.join(test_result_dir, 'e2e' + suffix)
                cmd = ['juju', 'scp', src, dest]
                subprocess.check_call(cmd)
        else:
            print('TEST_RESULT_DIR is not set, nowhere to put e2e results')

        self.assertEquals(outcome['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
