sudo add-apt-repository ppa:freecad-maintainers/freecad-stable
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    software-properties-common \
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
    libfreetype-dev \
    libhdf5-dev \
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
    libncurses-dev \
    libreadline-dev \
    libgl1-mesa-glx # This may not exist. Try ```sudo apt install libgl1```
