# ASK.md

Fill this in before you write any B2 code.

List up to five questions you would ask the product owner about B2 (the access check and the
cost-tagging check). Next to each one, write the assumption you'll build on until you get an
answer.

#

Question

Assumption I'll make

1

Should a Property Manager access screening reports belonging to another landlord account?

No. Access is restricted to the manager's assigned landlord_account_id.

2

How should the system behave if the tenant, property, or associated landlord information is missing?

Fail closed and deny access.

3

Should the access check validate ownership through the Tenant → Property → LandlordAccount relationship?

Yes. The report's tenant is resolved to its property, and the property's landlord account is compared with the manager's landlord account.

4

Which tag should be treated as the actual billing identifier when validating AWS resources?

landlord_account_id, because LandlordAccount is the billing unit.

5

Should resources with no tags, empty tags, or missing landlord_account_id fail the cost-tagging check?

Yes, for taggable resources being created or changed. Resources without a tags field, and resources that are only deleted or unchanged, should be skipped.
