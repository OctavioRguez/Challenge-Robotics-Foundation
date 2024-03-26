# Challenge-Robotics-Foundation

This project is a ROS (Robot Operating System) melodic package. It is currently at version 1.0.0.

## Description

This package provides interfaces and controllers for managing a motor with encoder for following a certain reference (signal). It includes PID controllers, signal generators, and hardware interface adapters.

## Installation

To install this package, clone the repository into your catkin workspace and build it using catkin.

```bash
cd ~/catkin_ws/src
git clone https://github.com/OctavioRguez/Challenge-Robotics-Foundation.git
cd ..
mv ./Challenge-Robotics-Foundation ./challenge_robotics_foundation
catkin_make
```

## Usage
To run the package, use the following command:
```
roslaunch challenge_robotics_foundation motor.launch
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Maintainer
This project is maintained by OctavioRguez. For any queries, you can reach out at octaviomacias16@hotmail.com.