import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mde_installed(host):
    assert host.package("mdatp").is_installed


def test_mde_install_log(host):
    assert host.file("/var/log/microsoft/mdatp/install.log").exists


def test_mde_group(host):
    assert host.group("mdatp").exists


def test_mde_user(host):
    assert host.user("mdatp").exists


def test_mde_service(host):
    service = host.service("mdatp")

    assert service.is_enabled
