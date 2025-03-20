#!/bin/bash

# Enable EPEL repository
sudo dnf install -y epel-release

# Install system packages
sudo dnf install -y \
    gcc \
    gcc-c++ \
    make \
    cmake \
    curl \
    git \
    pkgconfig \
    openssh-clients \
    sudo \
    unzip \
    wget \
    freetype-devel \
    hdf5-devel \
    zeromq3-devel \
    libjpeg-devel \
    libpng-devel \
    libX11-devel \
    libXext-devel \
    libXrender-devel \
    libffi-devel \
    sqlite-devel \
    bzip2-devel \
    ffmpeg \
    python3-tkinter \
    xz-devel \
    ninja-build \
    mesa-libOSMesa-devel \
    boost-devel \
    potrace \
    xorg-x11-server-Xvfb \
    ncurses-devel \
    ncurses-compat-libs \
    readline-devel \
    mesa-libGL-devel

# Install CUDA (if needed)
# Note: CUDA installation might need to be handled separately as it requires NVIDIA drivers
# and specific repository setup

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install DVC
# For RHEL, we'll need to use pip to install DVC as the deb repository won't work
sudo dnf install -y python3-pip
sudo pip3 install dvc

# Configure AWS credentials
export AWS_PROFILE=narnia-joe

# Create necessary directories
mkdir -p /dhh_bpc/dhh_bpc_ai/config
mkdir -p /dhh_bpc/.dvc
cd /dhh_bpc
git init -q

# Note: You'll need to copy your DVC configuration files here
# copy dvc config file to /dhh_bpc/.dvc
# copy weights.dvc, datasets.dvc, widgets.dvc to /dhh_bpc/dhh_bpc_ai

# Run DVC pull
dvc pull

# Set permissions
sudo chmod -R a+rw /dhh_bpc 
