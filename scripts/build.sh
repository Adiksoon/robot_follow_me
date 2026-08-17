#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose up -d ros2
  docker compose exec -T ros2 bash -lc '
    set -e
    source /opt/ros/humble/setup.bash
    cd /root/ros2_ws
    colcon build --symlink-install
  '
else
  source /opt/ros/humble/setup.bash
  colcon build --symlink-install
fi
