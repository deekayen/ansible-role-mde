import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mdatp_installed(host):
    assert host.package("mdatp").is_installed


def test_mdatp_etc(host):
    assert host.file("/etc/opt/microsoft/mdatp/mdatp_onboard.json").exists


def test_mdatp_logs(host):
    for filename in (
        ("/var/log/microsoft/mdatp_install.log"),
    ):
        log = host.file(filename)
        assert log.exists


def test_mdatp_service(host):
    service = host.service("mdatp")

    assert service.is_enabled


def test_mdatp_connectivity(host):
    cmd = host.run("mdatp connectivity test")

    assert cmd.succeeded


def test_mdatp_health(host):
    cmd = host.run("mdatp health")

    assert cmd.succeeded
