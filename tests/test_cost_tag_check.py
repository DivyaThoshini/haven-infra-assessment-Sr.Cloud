"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json flags the resources that are
     missing `landlord_account_id` and passes the rest. Work out the right result for every
     entry in the fixture from the rules in scripts/cost_tag_check.py.
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

Use a test double / your own in-memory plan dict where you don't need a real file on disk —
you don't need to shell out to the real script for every case.
"""
from scripts.cost_tag_check import check_plan
