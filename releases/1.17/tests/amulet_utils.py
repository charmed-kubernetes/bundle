import subprocess
import time
import yaml

from amulet.helpers import TimeoutError


def wait(sentry, timeout=900):
    """Waits for all units to be active/idle."""
    def check_status():
        status = sentry.get_status()
        for service_name in sentry.service_names:
            service = status.get(service_name, {})
            for unit_name, unit in service.items():
                if not unit['agent-status']:
                    return False
                if not unit['workload-status']:
                    return False
                if unit['agent-status'].get('current') != 'idle':
                    return False
                if unit['workload-status'].get('current') != 'active':
                    return False
        return True
    t0 = time.time()
    while time.time() - t0 < timeout:
        if check_status():
            return
        time.sleep(1)
    raise TimeoutError()


def attach_resource(charm, resource, resource_path):
    ''' Upload a resource to a deployed model.
    :param: charm - the application to attach the resource
    :param: resource - The charm's resouce key
    :param: resource_path - the path on disk to upload the
    resource'''

    # the primary reason for this method is to replace a shell
    # script in the $ROOT dir of the charm
    cmd = ['juju', 'attach', charm, "{}={}".format(resource, resource_path)]

    # Poll the controller to determine if resource placement is needed
    if not _has_resource(charm, resource):
        subprocess.call(cmd)


def check_systemd_service(unit, service):
    '''Return true if the systemd service is running and enabled. If it is not
    active, get the journal for that service.'''
    systemctl_is_active = 'systemctl is-active {0}'
    output, active = run(unit, systemctl_is_active.format(service))
    if active != 0:
        journalctl = 'journalctl -u {0}'
        run(unit, journalctl.format(service))
    systemctl_is_enabled = 'systemctl is-enabled {0}'
    output, enabled = run(unit, systemctl_is_enabled.format(service))
    return active == 0 and enabled == 0


def get_leader(units):
    """Return the leader unit for the array of units."""
    for unit in units:
        out = unit.run('is-leader')
        if out[0] == 'True':
            return unit


def kubectl(command, kubeconfig='', namespace='', json=False):
    '''Run kubectl commands and return the output and return code.'''
    kubectl = '/snap/bin/kubectl'
    # Is there a kubeconfig to use?
    if kubeconfig:
        # Append the kubeconfig flag and path.
        kubectl = '{0} --kubeconfig={0}'.format(kubectl, kubeconfig)
    # Is there a namespace to use?
    if namespace:
        # Append the namespace flag and namespace.
        kubectl = '{0} --namespace={1}'.format(kubectl, namespace)
    # Does the output need to be JSON?
    if json:
        # Append the output flag to the command
        kubectl = '{0} --output=json'.format(kubectl)
    return '{0} {1}'.format(kubectl, command)


def run(unit, command):
    '''Print out the command, run the command and print out the output.'''
    # Print the command so the results show what command was run.
    print(command)
    # Run the command on the unit.
    output, rc = unit.run(command)
    # Return the output and return code.
    return output, rc


def valid_certificate(unit, path):
    '''Return true if the certificate is valid, false otherwise.'''
    # Getting a large number of certificates would be expensive, this code
    # just verifies the file exists and contains valid being and end.
    output, begin = unit.run('grep "BEGIN CERTIFICATE" {0}'.format(path))
    output, end = unit.run('grep "END CERTIFICATE" {0}'.format(path))
    return begin == 0 and end == 0


def valid_key(unit, path):
    '''Return true if the file at path is a valid key.'''
    # Getting a large number of key files would be expensive, this code
    # just verifies the file exists and contains a valid begin and end.
    output, begin = unit.run('grep "BEGIN PRIVATE KEY" {0}'.format(path))
    output, end = unit.run('grep "END PRIVATE KEY" {0}'.format(path))
    return begin == 0 and end == 0


def _has_resource(charm, resource):
    ''' Poll the controller to determine if we need to upload a resource
    '''
    cmd = ['juju', 'resources', charm, '--format=yaml']
    output = subprocess.check_output(cmd)
    resource_list = yaml.safe_load(output)
    for resource in resource_list['resources']:
        # We can assume this is the correct resource if it has a filesize
        # matches the name of the resource in the charms resource stream
        if 'name' in resource and (charm in resource['name'] and
                                   resource['size'] > 0):
            # Display the found resource
            print('Uploading {} for {}'.format(resource['name'], charm))
            return True
    return False
