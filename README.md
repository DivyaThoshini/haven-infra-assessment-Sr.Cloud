# Haven — Platform Infrastructure Assessment

Haven is a multi-tenant real estate platform.

## Domain model

```
LandlordAccount  (the billing unit)
  └── Property
        └── Tenant
              └── ScreeningReport  (SSN, credit score)

PropertyManager  (scoped to exactly one LandlordAccount)
```

A `LandlordAccount` is the billing unit — every property, every tenant, every report underneath
it rolls up to exactly one. A `PropertyManager` is scoped to exactly one `LandlordAccount` and
everything under it.

This codebase currently tags and checks access using whatever ID happened to be on hand when
each piece was written — that reflects how it was built, not a spec to replicate.

## Setup

Use this repository as a template, create your own repository from it, and push your work there.
Pushing runs the checks in `.github/workflows/verify.yml`.

You need:

- Python 3.11 or newer
- Docker, `kubectl` and [`kind`](https://kind.sigs.k8s.io/) for B0 (on Windows, use WSL or Git
  Bash)

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

For B0, the commands `scripts/verify_b0.sh` runs, one at a time:

```bash
kind create cluster --name haven
docker build -t haven/photo-api:dev service/
kind load docker-image haven/photo-api:dev --name haven
kubectl apply -f k8s/
kubectl -n haven get pods
kubectl -n haven port-forward svc/photo-api 8080:80    # then: curl localhost:8080/
```

## What not to modify

`app/seed_data.py`, `app/models.py`, `fixtures/plan.json` and everything under `service/` — the
assignment's checks assume these are unchanged. Do B0 by changing `k8s/` only.

## Where things are

| Path | Task |
|---|---|
| `k8s/`, `service/`, `B0.md` | B0 |
| `ASK.md` | Fill in before B2 |
| `app/access_control.py`, `scripts/cost_tag_check.py` | B2 — stubs to implement |
| `mcp_server/` | B3 — you create this |
| `TERMINAL_LOG.md` | B0 before/after output (you create this) |
| `DESIGN_NOTES.md` | B2 idempotency key and B3 questions |

## Recording

Recording link: <!-- paste your link here -->
