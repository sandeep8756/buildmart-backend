#!/usr/bin/env bash
# Step 1: Build all 6 microservice Docker images.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="${REGISTRY:-ghcr.io/sandeep8756}"
TAG="${TAG:-latest}"

SERVICES=(
  "core/buildmart-materials/Dockerfile:core"
  "core/buildmart-workers/Dockerfile:core"
  "core/buildmart-delivery/Dockerfile:core"
  "bff/buildmart-materials-bff/Dockerfile:bff"
  "bff/buildmart-workers-bff/Dockerfile:bff"
  "bff/buildmart-delivery-bff/Dockerfile:bff"
)

echo "==> Building images (registry=$REGISTRY tag=$TAG)"

for entry in "${SERVICES[@]}"; do
  dockerfile="${entry%%:*}"
  layer="${entry#*:}"
  name="$(basename "$(dirname "$dockerfile")")"

  echo "  Building $REGISTRY/$name:$TAG"
  docker build \
    -f "$ROOT/$dockerfile" \
    -t "$REGISTRY/$name:$TAG" \
    "$ROOT/$layer"
done

echo "==> Build complete"
docker images | grep buildmart || true
