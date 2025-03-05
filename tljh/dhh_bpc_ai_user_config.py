"""
Configuration script for DHH BPC AI environment per user. Put this file in
/opt/tljh/config/jupyterhub_config.d/. The file inside /opt/tljh/config/jupyterhub_config.d/
can have any name, such as configure-my-setup.py. The important part is that it must have
a .py extension and contain valid Python code.

This script configures the user environment when a new JupyterHub instance is spawned.
It sets up symbolic links to shared resources and copies notebooks to the user's home directory.

The script includes:
- A first_time_setup function that runs once per user to:
  - Create symbolic links to shared config, widgets, datasets and weights
  - Copy notebooks from a central location to user's home directory
  - Create a flag file to prevent re-running the setup

The shared resources are expected to be in /dhh_bpc/dhh_bpc_ai/
Notebooks are copied from /dhh_bpc/notebooks/

This configuration is applied through JupyterHub's pre-spawn hook mechanism.
"""

import os
import subprocess
import shutil

def first_time_setup(spawner):
    user_home = spawner.user.home
    first_run_flag = os.path.join(user_home, ".first_run_done")

    if not os.path.exists(first_run_flag):
        # Create symbolic links
        links = {
            'config': '/dhh_bpc/dhh_bpc_ai/config',
            'widgets': '/dhh_bpc/dhh_bpc_ai/widgets',
            'datasets': '/dhh_bpc/dhh_bpc_ai/datasets',
            'weights': '/dhh_bpc/dhh_bpc_ai/weights'
        }
        
        for link_name, target in links.items():
            link_path = os.path.join(user_home, link_name)
            os.symlink(target, link_path)
        
        # Copy notebooks
        notebook_src = '/dhh_bpc/notebooks'
        for file in os.listdir(notebook_src):
            src_file = os.path.join(notebook_src, file)
            dst_file = os.path.join(user_home, file)
            shutil.copy2(src_file, dst_file)
            
        open(first_run_flag, "w").close()  # Create flag file to prevent reruns

c.Spawner.pre_spawn_hook = first_time_setup
