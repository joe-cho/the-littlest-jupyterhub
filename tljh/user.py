"""
User management for tljh.

Supports minimal user & group management
"""

import grp
import pwd
import subprocess
from os.path import expanduser
import os
import shutil

# Set up plugin infrastructure
from tljh.utils import get_plugin_manager

def setup_dhh_bpc_user(system_username):
    """
    Setup DHH BPC AI user environment by creating symbolic links to shared resources
    and copying notebooks to the user's home directory.
    
    Args:
        username (str): The username of the JupyterHub user
    """
    print(f"Setting up DHH BPC AI user environment for {system_username}")
    user_home = f"/home/{system_username}"
    first_run_flag = os.path.join(user_home, ".first_run_done")

    if not os.path.exists(first_run_flag):
        # Create symbolic links
        links = {
            'configs': '/dhh_bpc/configs',
            'datasets': '/dhh_bpc/datasets',
            'weights': '/dhh_bpc/weights',
            'widgets': '/dhh_bpc/widgets',
            'origin_notebooks': '/dhh_bpc/origin_notebooks',
        }

        for link_name, target in links.items():
            link_path = os.path.join(user_home, link_name)
            if not os.path.exists(link_path):
                os.symlink(target, link_path)

        # TODO: re-use later. A user had better copy them by himself.
        # Copy widget_code directory
        widget_code_src = '/dhh_bpc/widget_code'
        widget_code_dst = os.path.join(user_home, 'widget_code')
        if os.path.exists(widget_code_src):
            try:
                shutil.copytree(widget_code_src, widget_code_dst)
                # Change ownership using shell command
                subprocess.check_call(['chown', '-R', f'{system_username}:{system_username}', widget_code_dst])
                # Set permissions to 744 for all files
                subprocess.check_call(['chmod', '-R', '744', widget_code_dst])
                print("Successfully copied widget_code directory")
            except Exception as e:
                print(f"Error copying widget_code directory: {str(e)}")

        # Copy notebooks
        notebook_src = '/dhh_bpc/origin_notebooks'
        if os.path.exists(notebook_src):
            for file in os.listdir(notebook_src):
                try:
                    src_file = os.path.join(notebook_src, file)
                    dst_file = os.path.join(user_home, file)
                    shutil.copy2(src_file, dst_file)
                    # Change ownership and permissions using shell commands
                    subprocess.check_call(['chown', f'{system_username}:{system_username}', dst_file])
                    subprocess.check_call(['chmod', '744', dst_file])
                    print(f"Successfully copied {file}")
                except Exception as e:
                    print(f"Error copying {file}: {str(e)}")
            
        # Create flag file to prevent reruns
        open(first_run_flag, "w").close()
        print(f"DHH BPC AI user environment setup complete for {system_username}")

def ensure_user(username):
    """
    Make sure a given user exists
    """
    # Check if user exists
    try:
        pwd.getpwnam(username)
        # User exists, nothing to do!
        return
    except KeyError:
        # User doesn't exist, time to create!
        pass

    subprocess.check_call(["useradd", "--create-home", username])

    subprocess.check_call(["chmod", "o-rwx", expanduser(f"~{username}")])

    pm = get_plugin_manager()
    pm.hook.tljh_new_user_create(username=username)


def remove_user(username):
    """
    Remove user from system if exists
    """
    try:
        pwd.getpwnam(username)
    except KeyError:
        # User doesn't exist, nothing to do
        return

    subprocess.check_call(["deluser", "--quiet", username])


def ensure_group(groupname):
    """
    Ensure given group exists
    """
    subprocess.check_call(["groupadd", "--force", groupname])


def remove_group(groupname):
    """
    Remove group from system if exists
    """
    try:
        grp.getgrnam(groupname)
    except KeyError:
        # Group doesn't exist, nothing to do
        return

    subprocess.check_call(["delgroup", "--quiet", groupname])


def ensure_user_group(username, groupname):
    """
    Ensure given user is member of given group

    Group and User must already exist.
    """
    group = grp.getgrnam(groupname)
    if username in group.gr_mem:
        return

    subprocess.check_call(["gpasswd", "--add", username, groupname])


def remove_user_group(username, groupname):
    """
    Ensure given user is *not* a member of given group
    """
    group = grp.getgrnam(groupname)
    if username not in group.gr_mem:
        return

    subprocess.check_call(["gpasswd", "--delete", username, groupname])
