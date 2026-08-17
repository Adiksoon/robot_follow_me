# ROS 2 Interfaces

This document defines the intended boundaries between packages. It is a design contract, not a statement that every interface is implemented today.

## Frames

Target TF tree:

```text
odom
└── base_link
    └── camera_link
```

`odom -> base_link` is published by the odometry/state-estimation layer.
`base_link -> camera_link` is a fixed transform defined by the robot description once the real camera mount geometry is known.

Target observations used for control should ultimately be expressed relative to `base_link`.

## Existing / early-stage topics

### `/odom`

Type: `nav_msgs/msg/Odometry`

Producer: `piracer_control/odometry_node`

Consumers:

- `robot_control/follow_me_node`
- RViz/debug tooling

Purpose: robot pose and velocity estimate in the `odom` frame.

### `/cmd_ackermann`

Type: `ackermann_msgs/msg/AckermannDriveStamped`

Producer: `robot_control/follow_me_node`

Consumer: low-level PiRacer control / simulation adapter

Fields used:

- `drive.speed` — commanded longitudinal velocity
- `drive.steering_angle` — commanded steering angle

### `/image_raw`

Type: `sensor_msgs/msg/Image`

Producer:

- current test image publisher,
- later OAK-D/Gazebo camera source.

Consumer: `robot_perception/target_detection_node`

### `/target_detection`

Type: currently `vision_msgs/msg/Detection2DArray`

Producer: `robot_perception/target_detection_node`

Purpose: image-space target detections.

This interface must remain perception-only. High-level control should not depend directly on bounding boxes once target-pose estimation is available.

## Planned stable control-facing target interface

A target-pose stage should convert the selected detection and depth/distance estimate into a control-facing representation.

Preferred ROS-native option:

### `/target_pose`

Type: `geometry_msgs/msg/PoseStamped`

Frame: `base_link`

Producer: target-pose estimation stage in `robot_perception`

Consumer: `robot_control/follow_me_node`

Minimum semantics:

- pose is the selected target location relative to `base_link`,
- timestamp reflects the observation time,
- stale observations must not be treated as valid detections.

If additional metadata becomes necessary (confidence, target ID, explicit detection-valid flag), introduce a dedicated custom message instead of overloading `PoseStamped` fields.

## Planned target configuration interface

### `/target_config`

Producer: future `robot_calibration` / initialization component

Consumers:

- target detection/selection,
- high-level follow controller.

The exact message type is intentionally not frozen yet. It may contain:

- target class / identifier,
- desired following distance,
- detection threshold,
- operating mode.

Do not create a custom message until the required fields are confirmed by the implementation.

## Low-level hardware interfaces

The final hardware architecture should separate vehicle control from GPIO/PWM/encoder access.

Conceptual flow:

```text
/cmd_ackermann
      |
      v
PiRacer low-level controller
      |
      +--> motor command --> hardware interface --> PWM / motor driver
      |
      +--> steering command --> hardware interface --> steering servo

encoders --> hardware interface --> wheel-speed feedback --> odometry / speed loop
```

Exact topic names and message types should be finalized only when the real PiRacer I/O implementation is introduced.

## Simulation / hardware interchangeability rule

High-level packages (`robot_perception`, `robot_control`) should not need algorithm changes when switching between simulation and the real robot.

Prefer switching only:

- launch files,
- parameter files,
- sensor/actuator adapters,
- hardware-specific nodes.

## Safety contracts

The component that ultimately commands the real vehicle must enforce:

- maximum speed,
- maximum steering angle,
- command timeout,
- safe stop on stale command input,
- safe stop on shutdown.

The high-level follow controller must stop or enter a defined search state when target observations become stale.
