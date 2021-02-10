import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mdatp_installed(host):
    assert host.package("mdatp").is_installed


def test_mdatp_service(host):
    service = host.service("mdatp")

    assert service.is_enabled
