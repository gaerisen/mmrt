# MVSim/Navigation2 demo

`src/mvsim_demo` is a package containing only a launch file and related configs.
It does have dependencies, so make sure you run `rosdep install` before trying
to use it.

## Usage

In the root directory of the repo:

```bash
$ rosdep update && rosdep install -r --from-paths src --ignore-src
$ colcon build --packages-select mvsim_demo pointcloud_to_laserscan
$ source ./install/local_setup.bash
$ ros2 launch mvsim_demo launch.py
```

Config files are at `src/mvsim_demo/launch`. Edit them, then re-run lines 2 and
4 to experiment.

## Launchfile

The launchfile loads three major components:

1. `nav2_bringup`, a launchfile that ships with Navigation2 and starts the
   entire navigation stack based on the configuration in `nav2_params.yaml`.
   This file is built-in to the `mvsim_demo` package. Further discussion of its
   contents below.
2. `mvsim`, the simulation environment, configured by a world file that also
   ships with the demo package.
3. `rviz2`, the GUI. Also takes hints from `nav2_params.yaml` about what
   information is available to be presented to the user.

## Nav2 config

`nav2_params.yaml` is a behemoth config file defining dozens of parameters for
each of the several navigation components. There are likely entirely swaths of
these modules and config options that will never be relevant to us.

A couple notes to know about before getting into the weeds of things:

1. Transformations are a big part of how this stack operates. These are sets of
   coordinates, static or dynamic, indicating relative positions of several
   coordinate frames. We may end up having wuite a few of these on the rover
   itself, but the important ones are `map`, `odom`, and `base_link`. `map` is a
   fixed point on the global map. `odom` is the origin of the robot according to
   its odometry/localization stack. `base_link` is the robot's best guess of its
   own live pose.
2. Global costmaps and local costmaps are effectively the same thing, and can be
   configured to behave identically (in this demo, this is more or less how
   things are setup). The difference is in how they're used.
    1. Local costmaps are consumed by the collision monitor which sits at the
       end of the pipeline and overrides cmd_vel with its own values when it
       detects an imminent collision.
    2. The global costmap is consumed by the route planner, which allows
       rerouting around obstacles.

> One way to see the local/global distinction is to remove the voxel layer from
> one of the two and see how behavior changes; remove it from local, and the
> path will change to avoid obstacles but the robot may dip into the inflation
> layer slightly. Remove it from global, and the robot will refuse to collide
> with obstacles but won't be able to reroute around large ones.

A note on localization tooling:

AMCL is a localization engine based on Monte Carlo analysis (look it up). The
stated purpose of this is to account for drift in the odometry part of our
localization stack by using sensor data. Under the hood, it does this by
publishing the `map->odom` transformation. This is probably not useful to us,
which likely means we'll just publish a static `map->odom` transformation with
all 0 values.
