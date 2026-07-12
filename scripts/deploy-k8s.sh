#!/usr/bin/env bash
# Step 3: Deploy to Kubernetes — Core pods first, then BFF pods, then Ingress.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
K8S_DIR="$ROOT/k8s"
OUT_DIR="$ROOT/k8s/generated"

REGISTRY="${REGISTRY:-ghcr.io/sandeep8756}"
TAG="${TAG:-latest}"
API_HOST="${API_HOST:-api.buildmart.example.com}"
KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"

mkdir -p "$OUT_DIR"

render() {
  local src="$1"
  local dest="$2"
  sed -e "s|\${REGISTRY}|$REGISTRY|g" \
      -e "s|\${TAG}|$TAG|g" \
      -e "s|\${API_HOST}|$API_HOST|g" \
      "$src" > "$dest"
}

echo "==> Using kubeconfig: $KUBECONFIG"
echo "==> Registry: $REGISTRY  Tag: $TAG  API host: $API_HOST"

echo "==> Render manifests"
render "$K8S_DIR/namespace.yaml" "$OUT_DIR/namespace.yaml"
for f in "$K8S_DIR"/core/*.yaml; do
  render "$f" "$OUT_DIR/$(basename "$f")"
done
for f in "$K8S_DIR"/bff/*.yaml; do
  render "$f" "$OUT_DIR/$(basename "$f")"
done
render "$K8S_DIR/ingress.yaml" "$OUT_DIR/ingress.yaml"

echo "==> Apply namespace"
kubectl apply -f "$OUT_DIR/namespace.yaml"

echo "==> Deploy Core services (pods run internal ClusterIP)"
kubectl apply -f "$OUT_DIR/buildmart-materials.yaml"
kubectl apply -f "$OUT_DIR/buildmart-workers.yaml"
kubectl apply -f "$OUT_DIR/buildmart-delivery.yaml"
kubectl rollout status deployment/buildmart-materials -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-materials; exit 1; }
kubectl rollout status deployment/buildmart-workers -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-workers; exit 1; }
kubectl rollout status deployment/buildmart-delivery -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-delivery; exit 1; }

echo "==> Deploy BFF services (pods call Core via ip_port DNS)"
kubectl apply -f "$OUT_DIR/buildmart-materials-bff.yaml"
kubectl apply -f "$OUT_DIR/buildmart-workers-bff.yaml"
kubectl apply -f "$OUT_DIR/buildmart-delivery-bff.yaml"
kubectl rollout status deployment/buildmart-materials-bff -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-materials-bff; exit 1; }
kubectl rollout status deployment/buildmart-workers-bff -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-workers-bff; exit 1; }
kubectl rollout status deployment/buildmart-delivery-bff -n buildmart --timeout=300s || { kubectl describe pod -n buildmart -l app=buildmart-delivery-bff; exit 1; }

echo "==> Apply Ingress (public BFF URLs)"
kubectl apply -f "$OUT_DIR/ingress.yaml"

echo ""
echo "==> Deployment complete"
kubectl get pods,svc,ingress -n buildmart
echo ""
echo "BFF URLs for Vercel env vars:"
echo "  NEXT_PUBLIC_MATERIALS_BFF_URL=https://$API_HOST"
echo "  NEXT_PUBLIC_WORKERS_BFF_URL=https://$API_HOST"
echo "  NEXT_PUBLIC_DELIVERY_BFF_URL=https://$API_HOST"
