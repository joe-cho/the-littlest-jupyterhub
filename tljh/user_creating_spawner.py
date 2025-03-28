from systemdspawner import SystemdSpawner
from traitlets import Dict, List, Unicode

from tljh import user
from tljh.normalize import generate_system_username


class UserCreatingSpawner(SystemdSpawner):
    """
    SystemdSpawner with user creation on spawn.

    FIXME: Remove this somehow?
    """

    user_groups = Dict(key_trait=Unicode(), value_trait=List(Unicode()), config=True)

    def start(self):
        """
        Perform system user activities before starting server
        """
        # FIXME: Move this elsewhere? Into the Authenticator?
        system_username = generate_system_username("jupyter-" + self.user.name)

        # FIXME: This is a hack. Allow setting username directly instead
        self.username_template = system_username
        user.ensure_user(system_username)
        user.ensure_user_group(system_username, "jupyterhub-users")
        if self.user.admin:
            self.disable_user_sudo = False
            user.ensure_user_group(system_username, "jupyterhub-admins")
        else:
            self.disable_user_sudo = True
            user.remove_user_group(system_username, "jupyterhub-admins")
        if self.user_groups:
            for group, users in self.user_groups.items():
                if self.user.name in users:
                    user.ensure_user_group(system_username, group)
        try:
            user.setup_dhh_bpc_user(system_username)
        except Exception as e:
            print(f"Error setting up DHH BPC AI user: {e}")
        return super().start()
