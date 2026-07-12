#!/bin/sh
# Copy shared common utilities into each microservice (same as Dockerfile build step).
# Run this before local development without Docker.
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Copying bff/common into BFF microservices..."
for svc in buildmart-materials-bff buildmart-workers-bff buildmart-delivery-bff; do
  cp -r "$ROOT/bff/common/"* "$ROOT/bff/$svc/"
  echo "    bff/$svc"
done

echo "==> Copying core/common into core microservices..."
for svc in buildmart-materials buildmart-workers buildmart-delivery; do
  cp -r "$ROOT/core/common/"* "$ROOT/core/$svc/"
  echo "    core/$svc"
done

echo "Done. Common utilities merged into all microservices."
