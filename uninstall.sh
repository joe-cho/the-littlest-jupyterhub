sudo systemctl stop jupyter-joe.cho
sudo systemctl stop jupyter-dana.shin

sudo systemctl stop jupyterhub
sudo systemctl disable jupyterhub.service

sudo systemctl stop traefik
sudo systemctl disable traefik.service

sudo rm -rf /opt/tljh
sudo userdel -r jupyter-joe.cho
sudo userdel -r jupyter-dana.shin
