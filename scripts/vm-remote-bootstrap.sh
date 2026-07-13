#!/usr/bin/env bash
# Bootstrap Oracle Linux VM for M&P backend (podman-first, low RAM).
set -euo pipefail

echo "==> VM bootstrap"

# Free disk from failed deploy attempts
rm -f /home/opc/*.tar.gz /home/opc/docker-static.tgz 2>/dev/null || true
sudo dnf clean all 2>/dev/null || true
echo "Disk before deploy:"
df -h / /home/opc 2>/dev/null || df -h /

MEM_MB=$(free -m | awk '/^Mem:/{print $2}')
if [ "$MEM_MB" -lt 2048 ] && ! swapon --show 2>/dev/null | grep -q /swapfile; then
  echo "==> Adding 2GB swap (${MEM_MB}MB RAM)"
  sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=none
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
fi

if command -v podman >/dev/null; then
  echo "==> Using podman $(podman --version)"
  if ! podman compose version &>/dev/null 2>&1; then
    echo "==> Installing podman-compose (small package)"
    sudo dnf install -y podman-compose
  fi
  echo "COMPOSE_CMD=podman compose"
  exit 0
fi

echo "==> Podman missing; install podman"
sudo dnf install -y podman podman-compose
echo "COMPOSE_CMD=podman compose"
