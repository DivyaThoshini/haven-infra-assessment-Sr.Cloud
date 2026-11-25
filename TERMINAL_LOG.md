# TERMINAL_LOG.md

## B0 — Kubernetes Deployment Troubleshooting

### 1. Environment Setup

The following tools are required for local Kubernetes deployment:

- Docker
- Kind
- kubectl

### 2. Initial Investigation

Inspected the Kubernetes manifests and application source code.

Application findings:
- Application port: 8080
- Readiness endpoint: `/ready`
- Liveness endpoint: `/healthz`
- Configuration source: `haven-config` ConfigMap
- Kubernetes identity: `photo-api` ServiceAccount

### 3. Issues Identified

- Incorrect readiness probe path (`/health`).
- Incorrect liveness probe path (`/health`).
- Incorrect Service target port (`8081`).
- Missing RBAC permissions for reading the required ConfigMap.

### 4. Changes Implemented

- Updated readiness probe to `/ready`.
- Updated liveness probe to `/healthz`.
- Updated Service target port to `8080`.
- Added namespace-scoped Role and RoleBinding in `k8s/rbac.yaml`.

### 5. Before-Fix Diagnostic Output

The original pod description was not captured before the manifest changes. No before-fix output is reproduced here.

### 6. After-Fix Diagnostic Output

Pending execution of the deployment verification and collection of:

```bash
kubectl -n haven describe pod -l app=photo-api
```

### 7. Deployment Verification

Pending execution of:

```bash
bash scripts/verify_b0.sh
```

Actual command output and results will be added after execution.
