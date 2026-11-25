
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Validate landlord_account_id tags on taggable resources
    being created or updated in a Terraform JSON plan.

    Returns:
        0 if all applicable resources have the required tag.
        1 if any applicable resource is missing the tag.
    """

    try:
        with open(plan_path, "r", encoding="utf-8") as file:
            plan = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: Unable to read Terraform plan: {error}", file=sys.stderr)
        return 1

    missing_tags = []

    for resource in plan.get("resource_changes", []):
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Check only resources being created or updated.
        if not any(action in ("create", "update") for action in actions):
            continue

        after = change.get("after")

        if not isinstance(after, dict):
            continue

        # Skip resources that do not support tags.
        if "tags" not in after:
            continue

        # Prefer tags_all because it includes provider default tags.
        effective_tags = after.get("tags_all", after.get("tags"))

        if not isinstance(effective_tags, dict):
            effective_tags = {}

        landlord_account_id = effective_tags.get("landlord_account_id")

        if not isinstance(landlord_account_id, str) or not landlord_account_id.strip():
            missing_tags.append(resource.get("address", "<unknown-resource>"))

    if missing_tags:
        for address in missing_tags:
            print(f"MISSING landlord_account_id: {address}")
        return 1

    print("PASS: All applicable resources have landlord_account_id tags.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/cost_tag_check.py <plan.json>", file=sys.stderr)
        sys.exit(2)

    sys.exit(check_plan(sys.argv[1]))
