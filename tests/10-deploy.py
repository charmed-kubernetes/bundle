#!/usr/bin/python3

import amulet
import os
import unittest
import yaml

SECONDS_TO_WAIT = 1200


class TestCharm(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Read the bundle in and deploy the bundle."""
        # Get the relative bundle path from the environment variable.
        self.bundle = os.getenv('BUNDLE', 'bundle.yaml')
        # Create a path to the bundle based on this file's location.
        self.bundle_path = os.path.join(os.path.dirname(__file__),
                                        '..',
                                        self.bundle)
        # Normalize the path to the bundle.
        self.bundle_path = os.path.abspath(self.bundle_path)

        print('Deploying bundle: {0}'.format(self.bundle_path))

        self.deployment = amulet.Deployment()
        with open(self.bundle_path, 'r') as bundle_file:
            contents = yaml.safe_load(bundle_file)
            self.deployment.load(contents)

        # Allow some time for Juju to provision and deploy the bundle.
        self.deployment.setup(timeout=SECONDS_TO_WAIT)
        # Wait for the system to settle down.
        self.deployment.sentry.wait()

        self.k8s = self.deployment.sentry['kubernetes']
        self.etcd = self.deployment.sentry['etcd']

    def test_leader_exists(self):
        """Test that the kubernetes nodes have a master."""
        leader = get_leader(self.k8s)
        if not leader:
            message = 'No leader unit found, and there should be one.'
            raise Exception(message)

    def test_cluster_info(self):
        """Test that kubectl is installed and the cluster appears healthy."""
        for unit in self.k8s:
            output, rc = unit.run('kubectl cluster-info')
            if rc != 0:
                message = 'The kubectl command was unsuccessful: \n' + output
                raise Exception(message)
            if 'Kubernetes master' not in output:
                message = 'Kubernetes master is not running: \n' + output
                raise Exception(message)
            if 'KubeDNS' not in output:
                message = 'KubeDNS is not running: \n' + output
                raise Exception(message)

    def test_kube_containers(self):
        """Cycle through every unit in the service and ensure the kubernetes
        containers are running."""
        containers = ['apiserver', 'controller-manager', 'kubelet', 'proxy',
                      'scheduler']
        for unit in self.k8s:
            output, rc = unit.run('docker ps')
            if rc != 0:
                message = 'The docker command was not successful: \n' + output
                raise Exception(message)
            for container in containers:
                if container not in output:
                    print(output)
                    message = container + ' not found in docker processes.'
                    raise Exception(message)
        # Check if the leader is running the skydns service.
        leader = get_leader(self.k8s)
        output, rc = leader.run('docker ps')
        if rc != 0:
            message = 'The docker command was not successful: \n' + output
            raise Exception(message)
        for container in ['etcd', 'kube2sky', 'skydns', 'healthz']:
            if container not in output:
                print(output)
                message = container + ' not found in docker processes.'
                raise Exception(message)

    def test_tls_client_credentials_package(self):
        """The leader unit generates tls credentials. Test that the credentials
        are available and are a valid tar file."""

        unpack_path = '/tmp/'
        archive_path = '/home/ubuntu/kubectl_package.tar.gz'

        leader = get_leader(self.k8s)
        cmd = 'tar -xzvf {0} -C {1}'.format(archive_path, unpack_path)
        # Run the command to untar the package
        output, rc = leader.run(cmd)
        if rc != 0:
            message = 'The tar command was not successful: \n' + output
            raise Exception(message)


def get_leader(units):
    """Return the leader unit for the array of units."""
    for unit in units:
        out = unit.run('is-leader')
        if out[0] == 'True':
            return unit


if __name__ == '__main__':
    unittest.main()
