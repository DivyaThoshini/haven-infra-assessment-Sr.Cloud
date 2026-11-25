from app.models import PropertyManager, ScreeningReport, Property, Tenant


def can_access_screening_report(
    actor: PropertyManager,
    report: ScreeningReport,
    *,
    properties: list[Property],
    tenants: list[Tenant],
) -> bool:
    """
    Allow access only when the report's tenant belongs to a property
    under the PropertyManager's landlord account.

    Fail closed if the tenant or property cannot be found.
    """

    # Find the tenant associated with the screening report
    tenant = next(
        (t for t in tenants if t.id == report.tenant_id),
        None,
    )

    if tenant is None:
        return False

    # Find the property associated with the tenant
    property = next(
        (p for p in properties if p.id == tenant.property_id),
        None,
    )

    if property is None:
        return False

    # Compare landlord account ownership
    return property.landlord_account_id == actor.landlord_account_id
