"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after`.

Implement check_plan() so it:
  - Looks at every resource whose `change.actions` includes "create" or "update". A replace
    shows up as ["delete", "create"], so it counts. Skip everything else: "no-op", "read" and
    a pure "delete".
  - Only checks resources that can carry tags. An entry is taggable when `change.after` has a
    `tags` key (its value may be null or {}). An entry with no `tags` key, such as a lifecycle
    configuration, is not taggable and must not be flagged.
  - Reads a resource's effective tags from `tags_all` when that key is present, and from `tags`
    otherwise (provider default_tags only show up in `tags_all`).
  - Fails (returns a non-zero exit code) if the effective tags are missing `landlord_account_id`
    or it is blank. That tag identifies the real billing unit, per README.md's domain model —
    not whatever tag the resource happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Returns an exit code: 0 if every taggable resource being created/changed has a non-blank
    `landlord_account_id`, non-zero otherwise.
    """
    raise NotImplementedError("Implement this.")


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
