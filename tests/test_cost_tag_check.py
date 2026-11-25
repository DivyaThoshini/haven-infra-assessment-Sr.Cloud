
import json

from scripts.cost_tag_check import check_plan


def test_fixture_plan_reports_missing_billing_tags(capsys):
    result = check_plan("fixtures/plan.json")

    output = capsys.readouterr().out

    assert result == 1
    assert "aws_s3_bucket.listing_media" in output
    assert "aws_lambda_function.mls_feed_sync" in output
    assert "aws_s3_bucket.scratch" in output


def test_same_plan_is_idempotent(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.example",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {
                            "landlord_account_id": "la-001"
                        }
                    },
                },
            }
        ]
    }

    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    first_result = check_plan(str(plan_file))
    first_output = capsys.readouterr().out

    second_result = check_plan(str(plan_file))
    second_output = capsys.readouterr().out

    assert first_result == second_result == 0
    assert first_output == second_output


def test_tags_all_is_used_when_present(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.defaults",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {},
                        "tags_all": {
                            "landlord_account_id": "la-001"
                        },
                    },
                },
            }
        ]
    }

    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_file)) == 0
    assert "PASS" in capsys.readouterr().out


def test_untaggable_deleted_and_noop_resources_are_skipped(
    tmp_path, capsys
):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket_lifecycle_configuration.example",
                "change": {
                    "actions": ["create"],
                    "after": {"rule": []},
                },
            },
            {
                "address": "aws_s3_bucket.deleted",
                "change": {
                    "actions": ["delete"],
                    "after": None,
                },
            },
            {
                "address": "aws_s3_bucket.unchanged",
                "change": {
                    "actions": ["no-op"],
                    "after": {"tags": {}},
                },
            },
        ]
    }

    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_file)) == 0
    assert "PASS" in capsys.readouterr().out


def test_replacement_resource_is_checked(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.replacement",
                "change": {
                    "actions": ["delete", "create"],
                    "after": {"tags": {}},
                },
            }
        ]
    }

    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_file)) == 1
    assert "aws_s3_bucket.replacement" in capsys.readouterr().out


def test_blank_billing_tag_fails(tmp_path, capsys):
    plan = {
        "resource_changes": [
            {
                "address": "aws_s3_bucket.blank",
                "change": {
                    "actions": ["create"],
                    "after": {
                        "tags": {"landlord_account_id": "   "}
                    },
                },
            }
        ]
    }

    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps(plan), encoding="utf-8")

    assert check_plan(str(plan_file)) == 1
    assert "aws_s3_bucket.blank" in capsys.readouterr().out
