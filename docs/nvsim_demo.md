# MVSIM DEMO

`src/mvsim_demo` is a package containing only a launch file and related configs.
It does have dependencies, so make sure you run `rosdep install` before trying
to use it.

The launchfile loads three major components:

1. `nav2_bringup`, a launchfile that ships with Navigation2 and starts the
   entire navigation stack based on the configuration in `nav2_params.yaml`.
   This file is built-in to the `mvsim_demo` package. Further discussion of its
   contents below.
2. `mvsim`, the simulation environment, configured by a world file that also
   ships with the demo package.
3. `rviz2`, the GUI. Also takes hints from `nav2_params.yaml` about what
   information is available to be presented to the user.

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

Some of my findings on configuring the navigation stack that are both useful and
seem to be very hard to find:

- AMCL is a localization engine based on Monte Carlo analysis (look it up). The
  stated purpose of this is to account for drift in the odometry part of our
  localization stack by using sensor data. Under the hood, it does this by
  publishing the `map->odom` transformation. This is probably not useful to us,
  which likely means we'll just publish a static `map->odom` transformation with
  all 0 values.
