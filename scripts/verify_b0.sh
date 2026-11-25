#!/usr/bin/env bash
set -euo pipefail

CLUSTER="${CLUSTER:-haven}"
IMAGE="haven/photo-api:dev"

if ! kind get clusters 2>/dev/null | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER"
fi

docker build -t "$IMAGE" service/
kind load docker-image "$IMAGE" --name "$CLUSTER"

kubectl apply -f k8s/

kubectl -n haven rollout status deploy/photo-api --timeout=120s

kubectl -n haven port-forward svc/photo-api 18080:80 >/dev/null 2>&1 &
PF=$!
trap 'kill $PF 2>/dev/null || true' EXIT
sleep 3

BODY="$(curl -fsS http://127.0.0.1:18080/)"
echo "$BODY"
echo "$BODY" | grep -q '"max_upload_mb"' || { echo "FAIL: config not served" >&2; exit 1; }

READY="$(kubectl -n haven get pod -l app=photo-api -o jsonpath='{.items[0].status.containerStatuses[0].ready}')"
RESTARTS="$(kubectl -n haven get pod -l app=photo-api -o jsonpath='{.items[0].status.containerStatuses[0].restartCount}')"
[ "$READY" = "true" ] || { echo "FAIL: pod not ready" >&2; exit 1; }
echo "B0 OK (restarts: $RESTARTS)"
