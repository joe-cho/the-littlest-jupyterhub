sudo systemctl stop jupyterhub
sudo systemctl disable jupyterhub.service

sudo systemctl stop jupyterhub-joe.cho
sudo systemctl disable jupyterhub-joe.cho.service

sudo systemctl stop traefik
sudo systemctl disable traefik.service

sudo rm -rf /opt/tljh

