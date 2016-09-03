#!/usr/bin/python3

import amulet
import os
import time
import unittest
import yaml

SECONDS_TO_WAIT = 1200


class TestCharm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Read the bundle in and deploy the bundle."""
        # Get the relative bundle path from the environment variable.
        cls.bundle = os.getenv('BUNDLE', 'bundle.yaml')
        # Create a path to the bundle based on this file's location.
        cls.bundle_path = os.path.join(os.path.dirname(__file__),
                                       '..',
                                       cls.bundle)
        # Normalize the path to the bundle.
        cls.bundle_path = os.path.abspath(cls.bundle_path)

        print('Deploying bundle: {0}'.format(cls.bundle_path))

        cls.deployment = amulet.Deployment()
        with open(cls.bundle_path, 'r') as bundle_file:
            contents = yaml.safe_load(bundle_file)
            cls.deployment.load(contents)

        # Allow some time for Juju to provision and deploy the bundle.
        cls.deployment.setup(timeout=SECONDS_TO_WAIT)
        # Wait for the system to settle down.
        cls.deployment.sentry.wait()

        cls.k8s = cls.deployment.sentry['kubernetes']
        cls.etcd = cls.deployment.sentry['etcd']
        # Allow time for kubernetes to start the pods and services.
        cls.wait_for_kubectl(10, 120)

    @classmethod
    def wait_for_kubectl(cls, wait=30, max_wait=90):
        """Run kubectl and wait for correct return code before proceeding."""
        cmd = kubectl_cmd('cluster-info')
        k8s_leader = get_leader(cls.k8s)
        seconds = 0
        while seconds < max_wait:
            print(cmd)
            output, rc = k8s_leader.run(cmd)
            if rc != 0:
                print('Sleeping for {0} seconds.'.format(wait))
                time.sleep(wait)
                seconds += wait
            else:
                break
        if seconds >= max_wait:
            print('Wait exceeded {0} seconds'.format(max_wait))

    def test_leader_exists(self):
        """Test that the kubernetes nodes have a master."""
        leader = get_leader(self.k8s)
        if not leader:
            message = 'No leader unit found, and there should be one.'
            raise Exception(message)

    def test_cluster_info(self):
        """Test that kubectl is installed and the cluster appears healthy."""
        for unit in self.k8s:
            cmd = kubectl_cmd('cluster-info')
            print(cmd)
            output, rc = unit.run(cmd)
            print(output)
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
        containers = ['kubelet', 'proxy']
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
        # Check if the leader is running the leader containers.
        leader = get_leader(self.k8s)
        output, rc = leader.run('docker ps')
        if rc != 0:
            message = 'The docker command was not successful: \n' + output
            raise Exception(message)
        master_containers = ['apiserver', 'controller-manager', 'scheduler']
        for container in master_containers:
            if container not in output:
                print(output)
                message = container + ' not found in docker processes.'
                raise Exception(message)

    def test_kube_dns(self):
        """Cycle through the units to see if the kubedns container is running
        on one of them."""
        found_kubedns = False
        for unit in self.k8s:
            name = unit.info['unit_name']
            print(name)
            output, rc = unit.run('docker ps')
            print(output)
            if rc != 0:
                message = 'The docker command was not successful: \n' + output
                raise Exception(message)
            if 'kubedns' in output:
                found_kubedns = True
                break
        if not found_kubedns:
            message = 'kubedns was not found as a running container on nodes.'
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


def kubectl_cmd(command="", namespace="", json=False):
    """All the kubectl commands need the configuration appended."""
    cmd = 'kubectl --kubeconfig=/home/ubuntu/.kube/config'
    if namespace:
        cmd = '{0} --namespace={1}'.format(cmd, namespace)
    if json:
        cmd = '{0} --output=json'.format(cmd)
    return '{0} {1}'.format(cmd, command)

if __name__ == '__main__':
    unittest.main()
