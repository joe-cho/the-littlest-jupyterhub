## install apt packages system-wide.

export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y --no-install-recommends software-properties-common
sudo add-apt-repository ppa:freecad-maintainers/freecad-stable
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    ccache \
    cmake \
    curl \
    git \
    pkg-config \
    ssh \
    sudo \
    unzip \
    wget \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libzmq3-dev \
    libjpeg-dev \
    libpng-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    ffmpeg \
    python3-tk \
    liblzma-dev \
    ninja-build \
    libosmesa6-dev \
    libboost-all-dev \
    freecad \
    potrace \
    xvfb \
    cuda-toolkit-11-8 \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libgl1-mesa-glx

# install aws cli onto system-wide.
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# install dvc onto system-wide.
sudo wget \
       https://dvc.org/deb/dvc.list \
       -O /etc/apt/sources.list.d/dvc.list
wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg
sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/
rm -f packages.iterative.gpg
sudo apt update
sudo apt install dvc

# you should configure aws credentials as ```narnia-joe``` before running this.
export AWS_PROFILE=narnia-joe

# run dvc pull
# it takes so long time.
mkdir -p /dhh_bpc/dhh_bpc_ai/config
mkdir -p /dhh_bpc/.dvc
cd /dhh_bpc
git init -q

# Copy 
# copy dvc config file to /dhh_bpc/.dvc
# copy weights.dvc, datasets.dvc, widgets.dvc to /dhh_bpc/dhh_bpc_ai

# you should configure aws credentials before running this.
dvc pull

sudo chmod -R a+rw /dhh_bpc # make the directories writable by the user
