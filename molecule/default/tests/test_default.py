"""Testinfra checks for the Microsoft Defender for Endpoint role."""

import pytest

ONBOARD = "/etc/opt/microsoft/mdatp/mdatp_onboard.json"


def test_mdatp_installed(host):
    assert host.package("mdatp").is_installed


def test_mdatp_account(host):
    assert host.group("mdatp").exists
    assert host.user("mdatp").exists


def test_mdatp_service_enabled(host):
    assert host.service("mdatp").is_enabled


def test_onboarding_extracted(host):
    onboard = host.file(ONBOARD)
    assert onboard.is_file
    assert onboard.user == "root"
    assert onboard.mode == 0o600


@pytest.mark.parametrize("name", ["microsoft", "microsoft-2025"])
def test_signing_keys_trusted(host, name):
    if host.exists("apt-get"):
        key = host.file(f"/etc/apt/keyrings/{name}.asc")
        assert key.is_file
        assert key.mode == 0o644
    else:
        keys = host.check_output("rpm -q gpg-pubkey --qf '%{VERSION}\\n'")
        short_ids = {"microsoft": "be1229cf", "microsoft-2025": "f748182b"}
        assert short_ids[name] in keys.lower().split()


def test_repository_configured(host):
    if host.exists("apt-get"):
        repo = host.file("/etc/apt/sources.list.d/microsoft-prod.list")
        assert repo.contains("signed-by=/etc/apt/keyrings/microsoft.asc")
    else:
        repo = host.file("/etc/yum.repos.d/microsoft-prod.repo")
        assert repo.contains("packages.microsoft.com/.*/prod/")
