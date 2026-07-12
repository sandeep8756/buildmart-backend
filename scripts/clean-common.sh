#!/bin/sh
# Remove common files copied into microservices (for clean git state).
# Does NOT remove service-specific files like utils/properties.py or application/.
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

COMMON_FILES="middleware.py requirements.txt"
COMMON_UTILS="common.py common_async.py common_properties.py decorators_async.py exceptions.py logging_cfg.py logging.conf"

clean_service() {
  target="$1"
  for f in $COMMON_FILES; do
    rm -f "$target/$f"
  done
  for f in $COMMON_UTILS; do
    rm -f "$target/utils/$f"
  done
}

echo "==> Cleaning BFF microservices..."
for svc in buildmart-materials-bff buildmart-workers-bff buildmart-delivery-bff; do
  clean_service "$ROOT/bff/$svc"
  echo "    bff/$svc"
done

echo "==> Cleaning core microservices..."
for svc in buildmart-materials buildmart-workers buildmart-delivery; do
  clean_service "$ROOT/core/$svc"
  echo "    core/$svc"
done

echo "Done."
