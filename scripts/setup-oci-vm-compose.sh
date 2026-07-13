#!/usr/bin/env bash
# Simpler fix: Docker Compose on Oracle VM (no Kubernetes).
# Run on VM as opc user.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/sandeep8756/buildmart-backend.git}"
VM_IP="${VM_IP:-$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')}"

echo "==> M&P VM + Docker Compose setup"

MEM_MB=$(free -m | awk '/^Mem:/{print $2}')
if [ "$MEM_MB" -lt 2048 ] && ! swapon --show 2>/dev/null | grep -q /swapfile; then
  echo "==> Adding 2GB swap (VM has ${MEM_MB}MB RAM)"
  sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=none
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
fi

if ! command -v docker &>/dev/null; then
  sudo dnf install -y docker-engine git curl
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
  echo "Log out and back in, then re-run this script."
  exit 0
fi

if ! docker compose version &>/dev/null; then
  sudo dnf install -y docker-compose-plugin || sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
fi

if [ ! -d buildmart-backend ]; then
  git clone "$REPO_URL"
fi
cd buildmart-backend
git pull origin main || true

docker compose pull || docker compose build
docker compose up -d

echo ""
echo "==> Services running"
docker compose ps
echo ""
echo "VM IP: $VM_IP"
echo "Test:"
echo "  curl http://$VM_IP:8101/buildmart-materials-bff/materials_list_bff"
echo ""
echo "Vercel env vars:"
echo "  NEXT_PUBLIC_MATERIALS_BFF_URL=http://$VM_IP:8101"
echo "  NEXT_PUBLIC_WORKERS_BFF_URL=http://$VM_IP:8102"
echo "  NEXT_PUBLIC_DELIVERY_BFF_URL=http://$VM_IP:8103"
