# Design Notes

## B2 — Idempotency Key

The cost-tagging check uses the Terraform plan content as its input.

**Idempotency approach:**

- The check is read-only and does not modify the Terraform plan.
- It does not maintain external state or persist previous execution results.
- For an unchanged plan, repeated executions produce the same validation result, exit code and diagnostic output.
- The logical idempotency key is the unchanged Terraform plan content supplied to the checker.
- No separate database, cache or external idempotency store is required.

This ensures that running the cost-tagging check multiple times against the same plan is deterministic and idempotent.

## B2 — Screening Report Access Control

- Access is validated using the relationship ScreeningReport → Tenant → Property → LandlordAccount.
- A Property Manager can access reports only when the property's `landlord_account_id` matches their own.
- Missing tenant or property relationships fail closed.
- The implementation uses the supplied seed data and does not modify it.

## B2 — Cost Tagging Validation

- `landlord_account_id` is the required billing tag because LandlordAccount is the billing unit.
- Resources being created or updated are checked.
- Replacement operations are checked because they include a create action.
- Resources without a tags field, pure deletions and no-op changes are skipped.
- `tags_all` is preferred when present because it includes provider default tags.
- Missing, null, empty or whitespace-only billing tags fail validation.

## Other Design Decisions

- Kubernetes B0 uses namespace-scoped RBAC rather than cluster-wide permissions.
- The photo-api ServiceAccount receives only `get` permission on the `haven-config` ConfigMap.
- The application source code and protected seed data remain unchanged.
