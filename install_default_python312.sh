sudo dnf config-manager --set-enabled crb
sudo dnf install -y epel-release
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --set-enabled devel

sudo dnf install -y python3.12 python3.12-devel

sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 20
