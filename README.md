Deploy Microsoft Defender Endpoint for Linux
===========

[![CI](https://github.com/deekayen/ansible-role-mde/workflows/CI/badge.svg)](https://github.com/deekayen/ansible-role-mde/actions?query=workflow%3ACI) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

[Deploy Microsoft Defender for Endpoint for Linux](https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-atp/linux-install-with-ansible).

If an error occurs during installation, the installer will only report a general failure. The detailed log will be saved to `/var/log/microsoft/mdatp/install.log`.


Dependencies
------------

* curl
* unzip
* apt-transport-https (debian)
* gnupg (debian)
* python-apt (debian)


Default Variables
-----------------

Onboarding source supports replacing with a URL and expects the zip file downloaded from the Microsoft Defender Security Center device management onboarding website. This role expects you'll host that file internally on an artifact server like Nexus or as an unauthenticated LFS git object. If you keep the default `onboarding_source` value, it will deposit an empty json configuration file.

    channel: prod
    onboarding_source: "{{ role_path }}/files/WindowsDefenderATPOnboardingPackage.zip"
    uninstall: false

From the Microsoft documentation:

> Defender for Endpoint for Linux can be deployed from one of the following channels (denoted below as [channel]): insiders-fast, insiders-slow, or prod. Each of these channels corresponds to a Linux software repository.
>
> The choice of the channel determines the type and frequency of updates that are offered to your device. Devices in insiders-fast are the first ones to receive updates and new features, followed later by insiders-slow and lastly by prod.


Example Playbook
----------------

This example presumes you have a Sonatype Nexus server where you uploaded the onboarding package to a raw repository named *infosec-hosted*.

    ---

    - name: Install Microsoft Defender Endpoint for Linux.
      hosts: all:!platform_windows

      vars:
        onboarding_source: https://nexus.example.com/repository/infosec-hosted/mde/WindowsDefenderATPOnboardingPackage_Linux_Mgmt_Tool.zip

      roles:
        - deekayen.mde


Tags
----

* debian
* redhat
* repo
* package
* dependencies
* onboarding

License
-------

BSD
