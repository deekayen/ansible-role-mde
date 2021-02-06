Deploy Microsoft Defender for Endpoint
===========

[![CI](https://github.com/deekayen/ansible-role-mdatp/workflows/CI/badge.svg)](https://github.com/deekayen/ansible-role-mdatp/actions?query=workflow%3ACI) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

[Deploy Microsoft Defender for Endpoint for Linux](https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-atp/linux-install-with-ansible).

If an error occurs during installation, the installer will only report a general failure. The detailed log will be saved to `/var/log/microsoft/mdatp_install.log`.


Dependencies
------------

curl

Default Variables
-----------------

    channel: prod
    onboarding_source: files/WindowsDefenderATPOnboardingPackage.zip

Example Playbook
----------------

    - hosts: servers
      roles:
        - deekayen.mdatp

License
-------

BSD
