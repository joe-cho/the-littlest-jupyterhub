"""
Utilities for working with package managers (apt and dnf)
"""

import os
import subprocess
import platform

from tljh import utils

HERE = os.path.abspath(os.path.dirname(__file__))


def get_package_manager():
    """
    Detect the package manager to use based on the OS
    Returns 'apt' for Debian/Ubuntu and 'dnf' for RHEL/CentOS
    """
    if platform.system() != 'Linux':
        raise OSError("Only Linux systems are supported")

    # Check if running on RHEL/CentOS
    if os.path.exists('/etc/redhat-release'):
        return 'dnf'
    # Check if running on Debian/Ubuntu
    elif os.path.exists('/etc/debian_version'):
        return 'apt'
    else:
        raise OSError("Unsupported Linux distribution")


def trust_gpg_key(key):
    """
    Trust given GPG public key.

    key is a GPG public key (bytes) that can be passed to apt-key add via stdin.
    """
    # If gpg2 doesn't exist, install it
    if not os.path.exists("/usr/bin/gpg2"):
        install_packages(["gnupg2"])

    pm = get_package_manager()
    if pm == 'apt':
        utils.run_subprocess(["apt-key", "add", "-"], input=key)
    elif pm == 'dnf':
        # For dnf, we need to save the key to a temporary file first
        key_file = "/etc/pki/rpm-gpg/RPM-GPG-KEY-tljh"
        with open(key_file, "wb") as f:
            f.write(key)
        utils.run_subprocess(["rpm", "--import", key_file])


def add_source(name, source_url, section):
    """
    Add a package source.

    For apt: distro is determined from /etc/os-release
    For dnf: section is ignored as it's not used in RHEL
    """
    pm = get_package_manager()

    if pm == 'apt':
        # lsb_release is not installed in most docker images by default
        distro = (
            subprocess.check_output(
                ["/bin/bash", "-c", "source /etc/os-release && echo ${VERSION_CODENAME}"],
                stderr=subprocess.STDOUT,
            )
            .decode()
            .strip()
        )
        line = f"deb {source_url} {distro} {section}\n"
        with open(os.path.join("/etc/apt/sources.list.d/", name + ".list"), "a+") as f:
            # Write out deb line only if it already doesn't exist
            f.seek(0)
            if line not in f.read():
                f.write(line)
                f.truncate()
                utils.run_subprocess(["apt-get", "update", "--yes"])
    elif pm == 'dnf':
        # For dnf, we create a repo file using a template
        repo_file = f"/etc/yum.repos.d/{name}.repo"
        template_path = os.path.join(HERE, "templates", "repo.template")

        with open(template_path) as f:
            repo_template = f.read()

        repo_content = repo_template.format(
            name=name,
            baseurl=source_url
        )

        with open(repo_file, "w") as f:
            f.write(repo_content)
        utils.run_subprocess(["dnf", "clean", "all"])
        utils.run_subprocess(["dnf", "makecache"])


def install_packages(packages):
    """
    Install system packages using the appropriate package manager
    """
    pm = get_package_manager()

    if pm == 'apt':
        # Check if an apt-get update is required
        if len(os.listdir("/var/lib/apt/lists")) == 0:
            utils.run_subprocess(["apt-get", "update", "--yes"])
        env = os.environ.copy()
        # Stop apt from asking questions!
        env["DEBIAN_FRONTEND"] = "noninteractive"
        utils.run_subprocess(["apt-get", "install", "--yes"] + packages, env=env)
    elif pm == 'dnf':
        env = os.environ.copy()
        # Stop dnf from asking questions!
        env["DNF_FRONTEND"] = "noninteractive"
        utils.run_subprocess(["dnf", "install", "-y"] + packages, env=env)
