# Implementation Roadmap

The roadmap is ordered to reduce debugging complexity. Each stage should be testable before the next dependency is introduced.

## Stage 0 — Development environment

Goal: make the repository reproducible and friendly to human/Codex development.

- [x] ROS 2 Humble Docker base exists.
- [x] Docker Compose workspace mount exists.
- [x] Add root `AGENTS.md`.
- [x] Add project Codex configuration.
- [x] Add standard build/test scripts.
- [ ] Verify Docker + GUI + Gazebo from a clean WSL session.
- [ ] Add missing runtime/build dependencies to Dockerfile as they are confirmed.

Exit criterion: a fresh clone can be built using one documented command.

## Stage 1 — Robot model and deterministic simulation

Goal: establish a trustworthy simulated PiRacer before adding autonomous perception.

- [ ] Validate URDF/Xacro dimensions and joint structure.
- [ ] Confirm `base_link` and camera frame conventions.
- [ ] Spawn robot reliably in Gazebo Fortress.
- [ ] Drive simulated robot using `/cmd_ackermann` or a documented adapter.
- [ ] Verify TF and odometry in RViz2.
- [ ] Add a minimal deterministic test world.

Exit criterion: manual/open-loop Ackermann commands produce expected motion and TF/odometry.

## Stage 2 — State estimation and low-level vehicle model

Goal: remove test constants and establish the inner vehicle-control/state-estimation layer.

- [ ] Replace hard-coded odometry `v` and `phi` inputs.
- [ ] Define source of simulated wheel/vehicle velocity.
- [ ] Define source of real wheel velocity from encoders.
- [ ] Validate Ackermann odometry against simulator ground truth.
- [ ] Add bounds and invalid-`dt` handling tests.

Exit criterion: `/odom` follows known simulated trajectories within documented error bounds.

## Stage 3 — High-level follow controller with synthetic target

Goal: test control independently of computer vision.

- [ ] Refactor PID/controller mathematics into testable code independent of ROS callbacks.
- [ ] Replace hard-coded target errors with `/target_pose` input.
- [ ] Add configurable desired following distance.
- [ ] Add controller saturation and anti-windup.
- [ ] Add stale-target timeout.
- [ ] Add synthetic target-pose publisher for repeatable tests.
- [ ] Validate FOLLOW, SEARCH and STOP transitions.

Exit criterion: the simulated robot follows a synthetic moving target without any YOLO/OAK-D dependency.

## Stage 4 — Behavior Tree / decision logic

Goal: move high-level behaviour coordination into an explicit decision layer if required by the final thesis specification.

Candidate behaviours:

- target available -> FOLLOW,
- temporary target loss -> short tolerance,
- target lost -> SEARCH,
- target reacquired -> FOLLOW,
- prolonged loss / unsafe condition -> STOP.

Do not duplicate control mathematics inside the Behavior Tree. The tree should coordinate behaviours, while controller nodes perform control.

Exit criterion: behaviour transitions are deterministic and can be reproduced in simulation.

## Stage 5 — Perception pipeline using test data

Goal: develop the perception chain before relying on real hardware.

- [x] Basic ROS image publisher exists.
- [x] Initial detection node exists.
- [ ] Replace dummy detections with actual detection output.
- [ ] Define target-selection rule.
- [ ] Estimate horizontal target location.
- [ ] Integrate depth/distance estimation.
- [ ] Publish selected target pose in `base_link`.
- [ ] Handle confidence and stale detections.

Exit criterion: recorded/test images produce deterministic `/target_pose` outputs.

## Stage 6 — Gazebo end-to-end follow-me

Goal: combine simulation camera, perception, decision logic, and control.

- [ ] Add target object/person substitute to Gazebo scenario.
- [ ] Feed simulated camera/depth into perception.
- [ ] Run full perception -> target pose -> behaviour -> controller chain.
- [ ] Record rosbag data and experiment metadata.
- [ ] Define repeatable scenarios: straight follow, lateral movement, target loss, reacquisition.

Exit criterion: full system completes predefined simulation scenarios repeatably.

## Stage 7 — OAK-D Lite and real PiRacer

Goal: replace simulation adapters with real sensor/hardware adapters without changing high-level algorithms.

- [ ] Install and validate OAK-D Lite ROS integration.
- [ ] Define fixed `base_link -> camera_link` transform from measured mount geometry.
- [ ] Implement PiRacer hardware interface.
- [ ] Integrate motor PWM, steering servo and encoders.
- [ ] Implement speed/command limits and command watchdog.
- [ ] Tune inner-loop control.
- [ ] Tune outer-loop follow controller.

Exit criterion: the robot follows the selected target safely in controlled real-world tests.

## Stage 8 — Experiments and thesis evidence

Goal: produce defensible engineering evidence rather than anecdotal demonstrations.

Potential measured quantities:

- target-distance tracking error,
- lateral/angular tracking error,
- settling time,
- overshoot,
- target-reacquisition time,
- detection success rate under defined conditions,
- odometry error over defined trajectories,
- loop frequency / processing latency.

For every experiment store:

- scenario identifier,
- code commit SHA,
- parameter set,
- raw rosbag/logs,
- processed results,
- plot-generation script.

Never add numerical results before the corresponding experiment has actually been performed.
