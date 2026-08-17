# Robot Follow Me — Codex Agent Guide

## Project goal

Develop and validate a ROS 2 system for a modified Waveshare PiRacer that can detect, localize, search for, and follow a selected target. The system is validated in simulation first and then deployed to the real platform.

## Current stack

- Ubuntu 22.04
- ROS 2 Humble
- Ignition Gazebo / Gazebo Fortress
- Python 3
- ament_python
- Ackermann steering model
- OAK-D Lite / DepthAI planned for real perception
- vision_msgs for detections
- Docker development environment

## Read before changing code

Before making non-trivial changes, read:

1. `src/docs/ARCHITECUTRE.md`
2. `src/docs/PROJECT_STATE.md`
3. `src/docs/THESIS_CONCEPT.md`
4. the affected package's `package.xml`, `setup.py`, and source files

Treat the existing implementation as the source of truth for current progress. Do not replace working code with a completely new architecture unless the task explicitly requests a redesign.

## Existing ROS 2 package responsibilities

- `robot_description` — robot model, URDF/Xacro, TF-related description assets
- `robot_simulation` — simulation worlds, launch files, Gazebo integration
- `robot_perception` — image input, target detection and target-pose estimation
- `robot_control` — high-level follow-me behaviour and outer-loop control
- `piracer_control` — low-level PiRacer control and odometry
- future calibration / hardware-interface packages should remain separated from perception and high-level control

## Architecture rules

Keep the system modular and preserve the separation between:

1. perception,
2. decision making,
3. high-level motion control,
4. low-level vehicle control,
5. state estimation,
6. simulation,
7. hardware access.

Perception must not directly drive the vehicle.

Simulation and real hardware should expose equivalent ROS interfaces whenever practical so algorithms can be validated in simulation before hardware deployment.

Do not couple high-level control to YOLO-, OpenCV-, or DepthAI-specific implementation details. Convert perception results into stable ROS messages/interfaces first.

## Follow-me behaviour

The expected behaviour includes at least:

- following a detected target,
- short target-loss tolerance,
- searching for a lost target,
- stopping after a prolonged loss or unsafe condition.

The current `follow_me_node.py` already contains early FSM/PID logic. Improve it incrementally rather than silently replacing it.

## Control rules

- Keep controller math separate from ROS callbacks where practical.
- Controller parameters must become configurable ROS parameters before final experiments.
- Add output saturation for real hardware.
- Avoid integral wind-up.
- Handle invalid or excessive `dt` values.
- Stop safely when target data becomes stale.
- Never command unrestricted throttle on real hardware.

## Odometry rules

The odometry model uses Ackermann kinematics and publishes `odom -> base_link` plus `nav_msgs/msg/Odometry`.

Do not hard-code test velocity and steering in the final implementation. The production odometry node must use measured/commanded inputs documented in the architecture.

## Perception rules

The current perception package contains a test image publisher and an initial `target_detection_node`.

Develop perception in stages:

1. deterministic image/topic plumbing,
2. target detection,
3. target selection/identity handling,
4. distance estimation,
5. target pose in the robot coordinate system,
6. real OAK-D Lite integration.

Use simulation/test inputs when possible before depending on real camera hardware.

## Build and test

From the repository root use:

```bash
./scripts/build.sh
./scripts/test.sh
```

The scripts execute the ROS build/test inside the existing Docker development container when Docker Compose is available.

Do not claim a code task is complete unless the relevant build and tests were run, or explicitly state why they could not be run.

## Git workflow

- Make focused changes.
- Do not rewrite unrelated code.
- Prefer one logical task per commit/PR.
- Before large refactors, summarize the proposed change and its effect on ROS interfaces.
- Preserve compatibility with the existing `main` branch unless the task explicitly permits breaking changes.

## Thesis integrity

This repository supports an engineering thesis.

Never fabricate:

- experimental measurements,
- success rates,
- timings,
- FPS values,
- controller performance,
- simulation results,
- hardware results,
- bibliographic references.

If a result has not been measured, mark it as `TODO: MEASURE`.

Clearly separate:

- literature-backed statements,
- design decisions,
- implementation details,
- measured experimental observations,
- interpretation of results.

When a major implementation decision changes, update the relevant documentation.

## Definition of done

A task is done only when all applicable items are satisfied:

1. the intended behaviour is implemented,
2. the affected packages build,
3. relevant tests pass,
4. safety behaviour is preserved,
5. ROS interfaces remain documented,
6. documentation is updated when architecture changed,
7. no experimental or bibliographic information was invented.
