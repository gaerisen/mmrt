FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy

USER root

# ROS 2 requires a UTF-8 locale. Universe contains packages needed by ROS 2.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        locales \
        software-properties-common \
        curl \
        ca-certificates \
        gnupg \
        lsb-release \
        build-essential \
        cmake \
        gdb \
        python3-pip \
        python3-venv \
    && locale-gen en_US en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US:en

# Add the ROS 2 apt repository.
RUN apt-get update \
    && export ROS_APT_SOURCE_VERSION=$(curl -s \
    https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
    | grep -F "tag_name" | awk -F'"' '{print $4}') \
    && curl -L -o /tmp/ros2-apt-source.deb \
    "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. \
    /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" \
    && dpkg -i /tmp/ros2-apt-source.deb \
    && rm /tmp/ros2-apt-source.deb \
    && rm -rf /var/lib/apt/lists/*

# Install the ROS 2 Jazzy desktop distribution and common development tools.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ros-jazzy-desktop \
        ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep globally. The per-user database is refreshed after
# container creation by postCreateCommand in devcontainer.json.
RUN rosdep init

# Source ROS 2 automatically in interactive shells.
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" \
    >> /home/vscode/.bashrc \
    && chown vscode:vscode /home/vscode/.bashrc

USER vscode
WORKDIR /workspaces
