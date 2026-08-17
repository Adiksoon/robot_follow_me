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
    if [ -f install/setup.bash ]; then source install/setup.bash; fi
    colcon test --event-handlers console_direct+
    colcon test-result --verbose
  '
else
  source /opt/ros/humble/setup.bash
  if [ -f install/setup.bash ]; then source install/setup.bash; fi
  colcon test --event-handlers console_direct+
  colcon test-result --verbose
fi
