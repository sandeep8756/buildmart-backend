#!/usr/bin/env bash
# Full pipeline: build → release (push) → deploy pods to K8s
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export REGISTRY="${REGISTRY:-ghcr.io/sandeep8756}"
export TAG="${TAG:-$(git -C "$SCRIPT_DIR/.." rev-parse --short HEAD 2>/dev/null || echo latest)}"
export API_HOST="${API_HOST:-api.buildmart.example.com}"

echo "=== M&P Backend: Build → Release → Deploy ==="
echo "REGISTRY=$REGISTRY  TAG=$TAG  API_HOST=$API_HOST"
echo ""

"$SCRIPT_DIR/build-images.sh"
"$SCRIPT_DIR/push-images.sh"
"$SCRIPT_DIR/deploy-k8s.sh"

echo ""
echo "=== Pipeline complete ==="
