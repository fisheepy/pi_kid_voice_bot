#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="pi-kid-voice-bot.service"
SRC_PATH="deploy/systemd/${SERVICE_NAME}"
DST_PATH="/etc/systemd/system/${SERVICE_NAME}"

if [[ ! -f "${SRC_PATH}" ]]; then
  echo "Service template not found: ${SRC_PATH}" >&2
  exit 1
fi

sudo cp "${SRC_PATH}" "${DST_PATH}"
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

echo "Service installed and restarted: ${SERVICE_NAME}"
echo "Check status with: sudo systemctl status ${SERVICE_NAME}"
echo "Tail logs with: journalctl -u ${SERVICE_NAME} -f"
