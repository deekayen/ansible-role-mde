# deekayen.mde

[![CI](https://github.com/deekayen/ansible-role-mde/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-mde/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.mde-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/mde/) [![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that installs Microsoft Defender for Endpoint on Linux (the `mdatp` package) and onboards the host with the onboarding package from the Microsoft Defender portal. With `uninstall: true` it removes the package, the Microsoft repository and keys, and the onboarding configuration. It follows the manual repository method in Microsoft's [Deploy Microsoft Defender for Endpoint on Linux with Ansible](https://learn.microsoft.com/en-us/defender-endpoint/linux-install-with-ansible).

The role installs `unzip`, plus `curl` when `/usr/bin/curl` is missing, and on Debian-family hosts also `apt-transport-https`, `libplist-utils`, `python3-apt`, and `gnupg`. It trusts both Microsoft signing keys (`microsoft.asc` and `microsoft-2025.asc`). On Debian-family hosts it saves them to `/etc/apt/keyrings` and references them with `signed-by`, and on RedHat-family hosts it imports them into the RPM database by fingerprint. It then adds the `packages.microsoft.com` repository for the chosen channel as `microsoft-<channel>`, extracts the onboarding zip into `/etc/opt/microsoft/mdatp` with mode `0600`, and installs `mdatp`.

## Requirements

- ansible-core 2.15 or newer on the controller.
- Outbound HTTPS from the target to `packages.microsoft.com`, and to `onboarding_source` when it is a URL.
- Privilege escalation on the target. Run the play with `become: true`; the role installs packages, writes repository and key files, and writes under `/etc/opt/microsoft`.
- Fact gathering left on. The repository paths come from `ansible_facts.distribution`, `ansible_facts.distribution_major_version`, `ansible_facts.distribution_version`, and `ansible_facts.distribution_release`.
- An onboarding package from the Microsoft Defender portal for a host that should report to your tenant. The default placeholder is not one; see `onboarding_source` below.

## Supported platforms

From `meta/main.yml`, and each one runs through Molecule in CI:

| Platform | Versions |
| --- | --- |
| EL (Rocky Linux in CI) | 9, 10 |
| Amazon Linux | 2023 |
| Debian | 12 (bookworm), 13 (trixie) |
| Ubuntu | 22.04 (jammy), 24.04 (noble), 26.04 (resolute) |

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.mde
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.mde
    src: https://github.com/deekayen/ansible-role-mde.git
    scm: git
    version: main
```

```bash
ansible-galaxy role install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `channel` | `prod` | Defender release channel: `prod`, `insiders-fast`, or `insiders-slow` (enforced by `meta/argument_specs.yml`). Selects the repository path on RedHat-family hosts and the apt suite on Debian-family hosts, where `prod` uses the release codename. |
| `onboarding_source` | `{{ role_path }}/files/WindowsDefenderATPOnboardingPackage.zip` | Onboarding zip from the Microsoft Defender portal. An absolute path is read from the controller; an `http://` or `https://` URL is downloaded by the target. The role asserts it is one or the other. The default is a placeholder whose only file is an `mdatp_onboard.json` containing `{}`, so the host installs `mdatp` but is not onboarded to a tenant. |
| `uninstall` | `false` | When `true`, remove `mdatp`, the Microsoft repository and signing keys, and `/etc/opt/microsoft/mdatp`. |

`vars/main.yml` holds internal values: the install log path, the two signing key URLs and fingerprints, and the distribution name mappings for `packages.microsoft.com` paths.

## Behavior

- If `unarchive` cannot open the zip and reports `Failed to find handler`, the role treats that as success and continues. The next task then runs `/usr/bin/python3 /etc/opt/microsoft/mdatp/MicrosoftDefenderATPOnboardingLinuxServer.py` when `mdatp_onboard.json` is missing, and that fails if the script is absent.
- The role installs `mdatp` with `state: present`, so it does not upgrade an existing install.
- Changing `channel` on a host adds a second repository file named for the new channel and leaves the previous one in place. As of October 2026, Microsoft's [deployment guide](https://learn.microsoft.com/en-us/defender-endpoint/linux-install-with-ansible) says switching channels requires uninstalling and reinstalling the product.
- At verbosity 3 (`-vvv`), the role prints `/var/log/microsoft/mdatp/install.log` when it exists and is not empty.

## Dependencies

None.

## Example playbook

Onboarding package hosted on an internal Nexus raw repository:

```yaml
---
- name: Install Microsoft Defender for Endpoint.
  hosts: linux_servers
  become: true

  vars:
    onboarding_source: https://nexus.example.internal/repository/infosec-hosted/mde/WindowsDefenderATPOnboardingPackage.zip

  roles:
    - deekayen.mde
```

`nexus.example.internal` is a placeholder for your artifact server.

To remove Defender, run the same role with `uninstall: true`.

## Tags

| Tag | Tasks |
| --- | --- |
| `install`, `dependencies` | apt cache refresh and dependency packages. |
| `repo`, `debian`, `redhat` | Repository and signing key setup. |
| `onboarding` | Onboarding directory and extraction. |
| `package` | The `mdatp` package. |
| `debug` | Install log display. |

Input validation in `tasks/assert.yml` is tagged `always`. The `repo`, `debian`, `redhat`, `onboarding`, and `package` tags do not work with `--tags`; see [Known issues](#known-issues).

## Known issues

- The `include_tasks` calls in `tasks/main.yml:66`, `:69`, and `:72` have no tags. Under `--tags`, Ansible skips an untagged dynamic include, so `--tags repo`, `--tags onboarding`, or `--tags package` runs none of the tasks in `repository.yml`, `onboarding_setup.yml`, or `package.yml`. `--skip-tags` behaves as expected.
- `tasks/assert.yml:2-10` accepts any RedHat-family major version above 6, with the message "Only RedHat 7 and newer are supported." `tasks/main.yml:37-48` installs `audispd-plugins` on EL 8. `meta/main.yml` lists only EL 9 and 10, and CI tests neither EL 7 nor EL 8.

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint: `ansible-lint --profile production` and `flake8 molecule/`.
2. Molecule: converge, idempotence, and testinfra verification in Docker against each distribution in the table above, using the placeholder onboarding zip.

To run the same checks locally with Docker available:

```bash
pip3 install ansible-core ansible-lint flake8 molecule "molecule-plugins[docker]" docker pytest-testinfra
ansible-lint --profile production
flake8 molecule/
MOLECULE_DISTRO=rockylinux9 molecule test
```

`MOLECULE_DISTRO` selects a `geerlingguy/docker-<distro>-ansible` image. The values CI uses are `rockylinux9`, `rockylinux10`, `amazonlinux2023`, `ubuntu2204`, `ubuntu2404`, `ubuntu2604`, `debian12`, and `debian13`. The testinfra checks in `molecule/default/tests/test_default.py` confirm that `mdatp` is installed, the `mdatp` user and group exist, the `mdatp` service is enabled, `mdatp_onboard.json` is a root-owned `0600` file, both signing keys are trusted, and the `microsoft-prod` repository file points at `packages.microsoft.com`.

The repository also has a `.pre-commit-config.yaml`; run `pre-commit run --all-files` before pushing.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Dependencies, the three includes below, and install log display. |
| `tasks/assert.yml` | EL version and `onboarding_source` checks, tagged `always`. |
| `tasks/repository.yml` | Signing keys and the `packages.microsoft.com` repository. |
| `tasks/onboarding_setup.yml` | `/etc/opt/microsoft/mdatp` and onboarding zip extraction. |
| `tasks/package.yml` | Installs or removes `mdatp`. |
| `defaults/main.yml` | Every user-facing variable. |
| `vars/main.yml` | Signing keys, distribution name mappings, and the install log path. |
| `files/WindowsDefenderATPOnboardingPackage.zip` | Placeholder onboarding zip, excluded from Git LFS in `.gitattributes` so CI checkouts and Galaxy tarballs get the real file. |
| `meta/argument_specs.yml` | Argument spec, including the `channel` choices. |
| `molecule/default/` | Molecule scenario: `prepare.yml`, `converge.yml`, and testinfra tests. |
| `.github/workflows/` | `ci.yml` for lint and Molecule, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.mde`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen). Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).
