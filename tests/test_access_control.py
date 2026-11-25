from app.access_control import can_access_screening_report


def test_same_landlord_can_access_report(
    property_managers,
    properties,
    tenants,
    screening_reports,
):
    actor = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-001")

    assert can_access_screening_report(
        actor,
        report,
        properties=properties,
        tenants=tenants,
    ) is True


def test_different_landlord_cannot_access_report(
    property_managers,
    properties,
    tenants,
    screening_reports,
):
    actor = next(pm for pm in property_managers if pm.id == "pm-001")
    report = next(r for r in screening_reports if r.id == "rep-002")

    assert can_access_screening_report(
        actor,
        report,
        properties=properties,
        tenants=tenants,
    ) is False


def test_missing_tenant_denies_access(
    property_managers,
    properties,
):
    from app.models import ScreeningReport

    actor = property_managers[0]
    report = ScreeningReport(
        id="rep-missing",
        tenant_id="unknown-tenant",
        ssn_last4="1234",
        credit_score=700,
    )

    assert can_access_screening_report(
        actor,
        report,
        properties=properties,
        tenants=[],
    ) is False


def test_missing_property_denies_access(
    property_managers,
    tenants,
):
    from app.models import ScreeningReport

    actor = property_managers[0]
    report = ScreeningReport(
        id="rep-missing-property",
        tenant_id=tenants[0].id,
        ssn_last4="1234",
        credit_score=700,
    )

    assert can_access_screening_report(
        actor,
        report,
        properties=[],
        tenants=tenants,
    ) is False
