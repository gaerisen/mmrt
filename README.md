# MMRT

ROS2 packages for MMRTs 2026 rover

## Getting Started

This repo relies on ROS2 Jazzy Jalisco being installed. If you are on Ubuntu
24.04, follow the installation instructions for Jazzy
[here](https://docs.ros.org/en/jazzy/index.html), then continue with
[First Build]. If not, read on starting with [Dev Container Setup]

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

First, initialize and pull submodules:

```
$ git submodule init
$ git submodule update
```

Then install the necessary dependencies:

`$ rosdep install --from-paths src/`

The joystick demo node relies on the ODrive motor driver, so build that first:

```
$ colcon build --packages-select odrive_can
$ source ./install/local_setup.bash     # Adds freshly built modules to the
                                        # environment. You'll typically do this
                                        # after every build.
```

Then build the rest of the packages:

```
$ colcon build
$ source ./install/local_setup.bash
```
