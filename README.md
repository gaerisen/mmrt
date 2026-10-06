# MMRT

ROS2 packages for MMRTs 2026 rover

## Getting Started

This repo relies on ROS2 Jazzy Jalisco being installed. If you are on Ubuntu
24.04, follow the installation instructions for Jazzy
[here](https://docs.ros.org/en/jazzy/index.html), then continue with First
Build. If not, read on starting with Dev Container Setup.

### Dev Container Setup

Right now, this only works if you're using VS Code and have installed the
official Microsoft Dev Containers extension. You must also have Docker installed
on your system.

If you've done all these things correctly, VS Code should recognize a dev
container config when you open this repo in it. If there's a notification
offering to `Reopen Folder in Container`, select it. Otherwise, you should be
able to do it manually through the remote menu in the very bottom left. The
first time you do this, expect it to take several minutes.

Once you're (hopefully) in the container, open a terminal in VS Code and do a
quick round of updates:

```
$ sudo apt update && sudo apt upgrade
$ rosdep update
```

### First Build

Some packages depend on submodules that rosdep can't find on its own. First,
initialize and pull those submodules:

```
$ git submodule init
$ git submodule update
```

Then install all the dependencies rosdep *can* find:

`$ rosdep install -r --from-paths src/`

Then try your first build:

```
$ colcon build
```

You'll need to source the workspace's environment to let ROS2 see your
executables and launch files:

```
$ source ./install/local_setup.bash
```
