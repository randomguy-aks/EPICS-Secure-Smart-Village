# Cyber Security — Remediation Set 1

**Date:** 26 November 2026  
**Source branch:** `cs/security-hardening` (based on `ecommerce`)  
**Target branch:** `ecommerce`

## Changes in this pull request

### Implemented
- Removed the committed Django secret-key fallback from settings. The application now requires `DJANGO_SECRET_KEY` from the environment and fails with a clear configuration error if it is missing.
- Added environment-driven `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, trusted CSRF origins, HTTPS redirect, secure session/CSRF cookies, HSTS, and related browser security settings. Local development values are documented in `.env.example`; production values must be configured for the actual HTTPS host/proxy.
- Added HTTP-only session cookies, SameSite=Lax cookies, clickjacking protection, content-type sniffing protection, and a strict referrer policy.
- Seller dashboard now requires an active seller profile in addition to the seller account role.
- Product form only offers active categories.
- Cart stock checks now lock the inventory row inside the transaction before checking and changing the cart quantity, reducing concurrent stale-stock checks.

## Not changed intentionally
- Seller approval is still automatic in the current schema. Introducing a pending/approved/rejected state changes shared model behaviour and needs E-Commerce agreement plus a migration.
- Product creation still publishes immediately. Changing this is a marketplace workflow decision; E-Commerce must confirm the intended publish/review process.
- No organisation membership schema was added.
- No order/payment model or payment integration was added.
- No new packages or database migrations were introduced.

## Required action by each developer / deployment owner

1. Generate a fresh private key:
   `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
2. Put that value in the ignored repository-root `.env` as `DJANGO_SECRET_KEY=...`. Never commit it or paste it into chat.
3. The previously committed key must be considered exposed. Rotate it anywhere it was reused; changing the current file does not erase it from Git history.
4. For local development set `DJANGO_DEBUG=True` and `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]` in local `.env`.
5. For production, set `DJANGO_DEBUG=False`, an explicit `DJANGO_ALLOWED_HOSTS`, HTTPS, secure cookies, and trusted CSRF origins. Enable HSTS only after HTTPS is working correctly. Configure proxy headers only if the trusted proxy is known to sanitize them.
6. Run Django checks and the existing test suite in the actual project environment before merging.

## Review notes
- No shared database models or migrations were modified.
- This pull request must be reviewed by E-Commerce because it changes shared Django settings and cart/product/seller view behaviour.
- The changes have been committed to the CS branch but have not been executed against the team's local MySQL environment in this session.
