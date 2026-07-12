#!/usr/bin/env bash
# Step 2: Push built images to container registry (release).
set -euo pipefail

REGISTRY="${REGISTRY:-ghcr.io/sandeep8756}"
TAG="${TAG:-latest}"

IMAGES=(
  buildmart-materials
  buildmart-workers
  buildmart-delivery
  buildmart-materials-bff
  buildmart-workers-bff
  buildmart-delivery-bff
)

echo "==> Pushing images to $REGISTRY (tag=$TAG)"
echo "    Login first if needed:"
echo "    echo \$GITHUB_TOKEN | docker login ghcr.io -u sandeep8756 --password-stdin"

for img in "${IMAGES[@]}"; do
  echo "  Pushing $REGISTRY/$img:$TAG"
  docker push "$REGISTRY/$img:$TAG"
done

echo "==> Release complete"
