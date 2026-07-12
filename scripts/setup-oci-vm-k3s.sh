#!/usr/bin/env bash
# Install k3s + deploy M&P backend on Oracle Cloud Always Free VM.
# Run on the VM as opc user after SSH login.
set -euo pipefail

REGISTRY="${REGISTRY:-ghcr.io/sandeep8756}"
TAG="${TAG:-latest}"
API_HOST="${API_HOST:-$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')}"
REPO_URL="${REPO_URL:-https://github.com/sandeep8756/buildmart-backend.git}"

echo "==> M&P VM + k3s setup"
echo "    REGISTRY=$REGISTRY  TAG=$TAG  API_HOST=$API_HOST"

echo "==> Install Docker (for image pull)"
if ! command -v docker &>/dev/null; then
  sudo dnf install -y docker-engine git curl
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
  echo "Log out and back in, then re-run this script."
  exit 0
fi

echo "==> Install k3s"
if ! command -v k3s &>/dev/null; then
  curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode 644" sh -
fi

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
mkdir -p "$HOME/.kube"
cp /etc/rancher/k3s/k3s.yaml "$HOME/.kube/config"
chmod 600 "$HOME/.kube/config"

echo "==> Wait for node Ready"
kubectl wait --for=condition=Ready node --all --timeout=120s
kubectl get nodes

echo "==> Install NGINX Ingress"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/cloud/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s || echo "Ingress still starting..."

echo "==> Clone backend repo"
if [ ! -d buildmart-backend ]; then
  git clone "$REPO_URL"
fi
cd buildmart-backend
git pull origin main || true

echo "==> Deploy all services"
export REGISTRY TAG API_HOST KUBECONFIG
chmod +x scripts/deploy-k8s.sh
./scripts/deploy-k8s.sh

echo ""
echo "==> Setup complete"
echo "VM public IP: $API_HOST"
echo ""
echo "Open OCI Security List ports: 80, 443, 8101, 8102, 8103"
echo ""
echo "Vercel env vars:"
echo "  NEXT_PUBLIC_MATERIALS_BFF_URL=http://$API_HOST"
echo "  NEXT_PUBLIC_WORKERS_BFF_URL=http://$API_HOST"
echo "  NEXT_PUBLIC_DELIVERY_BFF_URL=http://$API_HOST"
echo ""
kubectl get pods,svc,ingress -n buildmart
