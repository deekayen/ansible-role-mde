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

Onboarding source supports replacing with a URL and expects the zip file downloaded from the Microsoft Defender Security Center device management onboarding website. This role expects you'll host that file internally on an artifact server like Nexus or as an unauthenticated LFS git object.

I know templating a jinja2 json file is also a potential route to upload configurations and would appreciate an elegant pull request to support something like that.

    channel: prod
    onboarding_source: "{{ role_path }}/files/WindowsDefenderATPOnboardingPackage.zip"
    uninstall: false

From the Microsoft documentation:

> Defender for Endpoint for Linux can be deployed from one of the following channels (denoted below as [channel]): insiders-fast, insiders-slow, or prod. Each of these channels corresponds to a Linux software repository.
>
> The choice of the channel determines the type and frequency of updates that are offered to your device. Devices in insiders-fast are the first ones to receive updates and new features, followed later by insiders-slow and lastly by prod.


Example Playbook
----------------

    - hosts: servers
      roles:
        - deekayen.mdatp

Tags
----

* debian
* redhat
* repo
* install
* dependencies
* onboarding
* uninstall

License
-------

BSD
