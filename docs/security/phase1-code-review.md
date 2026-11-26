# Cyber Security Phase 1 — Initial Code Review

**Review date:** 26 November 2026  
**Reviewed branch:** `ecommerce`  
**Review owner:** Cyber Security (CS)  
**Scope:** Read-only review of the current Django implementation. This document records findings from the files listed below; it does not claim a penetration test or production deployment review.

## Confirmed findings

| ID | Severity | Evidence | Finding and impact |
|---|---|---|---|
| CS-01 | Critical if this key has been used outside local development | `backend/config/settings.py` | A Django `SECRET_KEY` value is committed in source code. Anyone with repository access can read it. Rotate it, load the replacement from an environment variable, and ensure the old key is not reused. |
| CS-02 | High for any internet-facing deployment | `backend/config/settings.py` | `DEBUG = True` is hard-coded and `ALLOWED_HOSTS = []`. These are development-only settings and must be environment-controlled before deployment. |
| CS-03 | High — seller trust / marketplace integrity | `backend/sellers/models.py`, `backend/accounts/views.py` | `SellerProfile.is_active` defaults to `True`; seller registration creates the profile without a verification/approval state. The product listing view treats active sellers' published products as public. Unverified sellers can therefore become active immediately. |
| CS-04 | High — publication policy | `backend/products/views.py` | `add_product` explicitly sets `product.status = 'published'`, overriding the model's `draft` default. New products are published immediately rather than awaiting review or an explicit seller action. |
| CS-05 | Medium — authorization consistency | `backend/sellers/views.py` | `seller_dashboard` checks `AccountProfile.role == 'seller'` but does not check `SellerProfile.is_active`. An inactive seller profile can still access this view if the account role remains seller. |
| CS-06 | Medium — data validation | `backend/products/forms.py`, `backend/products/models.py` | The product form's category field uses the model relationship without an active-category restriction. Inactive categories can be selected unless another layer prevents it. The form's quantity field permits zero; confirm whether zero-stock listings should be accepted. |
| CS-07 | Medium — concurrency / inventory integrity | `backend/orders/views.py`, `backend/inventory/models.py` | `add_to_cart` reads stock before entering its transaction and locks the cart item, not the inventory row. Concurrent requests can both pass the stock check. Cart quantities are not a reservation, but stock validation should be rechecked under a suitable lock at checkout/order placement. |

## Existing positive controls observed

- Django's `CsrfViewMiddleware` is enabled in `backend/config/settings.py`.
- Seller logout, consumer logout, cart update, cart removal, and add-to-cart use POST-only decorators where inspected.
- Cart view/update/removal scope cart items through the cart belonging to `request.user`, preventing a user from addressing another consumer's cart item through these views.
- Seller product creation assigns `product.seller = seller` from the authenticated user's seller profile rather than accepting a seller ID from the form.
- Product price has server-side validation requiring a value greater than zero.
- Django's standard password validators are configured.

## Not yet verified

- Whether every HTML form includes a CSRF token; templates were not part of this pass.
- Whether production deployment overrides settings securely; deployment configuration was not inspected.
- Whether login endpoints have rate limiting / credential-stuffing protection.
- Whether admin access is restricted and protected with MFA.
- Whether user-controlled text is safely rendered in all templates.
- Whether inactive sellers can access other seller-only routes not yet implemented or inspected.
- Whether order placement will revalidate price, seller status, stock, and cart ownership. The current order model/checkout flow is not implemented in the reviewed branch.
- Whether API endpoints exist; the inspected project currently routes to Django views and forms. DRF is installed, but no serializers/API routes were found in the inspected files.

## Recommended remediation requirements

1. Rotate the exposed Django secret key; load it from the environment and fail safely when a production secret is absent.
2. Make `DEBUG`, `ALLOWED_HOSTS`, secure-cookie, HTTPS, HSTS, and proxy settings environment-specific. Do not enable production values blindly in local development.
3. Introduce an explicit seller verification/approval state and default new seller profiles to pending/inactive. Do not treat registration as verification.
4. Require an active, approved seller profile in every seller-only view and in public product querysets.
5. Agree with E-Commerce whether products should default to draft or require a seller publish action; remove the unconditional publish assignment if review/draft is the agreed policy.
6. Restrict product category choices to active categories and validate stock/quantity rules server-side.
7. At checkout/order creation, re-read and validate stock inside a transaction with appropriate row locking; do not treat adding an item to a cart as stock reservation.
8. Add tests for unauthenticated access, wrong-role access, inactive sellers, cross-user cart IDs, CSRF enforcement, invalid price/quantity/category, and concurrent stock updates.

## Coordination boundary

This is a CS review of the existing E-Commerce branch. Changes to shared models, seller approval fields, organisation membership, checkout/order models, or migrations must be agreed with E-Commerce before implementation. No shared model or E-Commerce source file was changed as part of this review.
