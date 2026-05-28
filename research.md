# Research: Best JWT Library for Django REST Framework (2025–2026)

## Summary

**`djangorestframework-simplejwt` remains the unquestioned standard** for JWT auth in Django REST Framework — ~7M monthly downloads, 4.3K GitHub stars, actively maintained under the Jazzband organization (latest release v5.5.1, July 2025). For this project, which already uses `AUTH_HEADER_PREFIX: "Bearer"` in Knox, the migration is relatively straightforward. The main breaking change is the login response format (Knox returns `{expiry, token}`; SimpleJWT returns `{access, refresh}`). Two newer alternatives exist — `django-tokenforge` (security-first, Knox-like settings, replay detection) and `jwtguard` (v0.1.1, too immature) — but neither has the ecosystem maturity of simplejwt.

---

## Findings

### 1. djangorestframework-simplejwt: The De Facto Standard

- **PyPI stats (May 2026):** ~7M downloads/month, ~1.7M/week, ~293K/day. [Source](https://pypi.org/project/djangorestframework-simplejwt/)
- **GitHub:** 4,315 stars, 701 forks, 130 contributors, 708 commits. Last push March 2026. [Source](https://github.com/jazzband/django-rest-framework-simplejwt)
- **Snyk score:** 82/100 — "Influential project," "Sustainable" maintenance, no known security issues. [Source](https://security.snyk.io/package/pip/djangorestframework-simplejwt)
- **Jazzband maintained** — community-backed, not dependent on a single maintainer.
- **Version 5.5.1** (July 2025) supports Django ≥4.2, DRF ≥3.14, PyJWT ≥1.7.1, Python ≥3.9.
- **Status:** Production/Stable on PyPI.
- **Verdict:** There is no credible competitor with comparable adoption. It is the safe, boring choice.

### 2. Alternatives Evaluated

| Library | Version | Stars | Status | Notes |
|---------|---------|-------|--------|-------|
| `djangorestframework-simplejwt` | 5.5.1 | 4,315 ⭐ | Active (Jazzband) | The standard |
| `django-rest-knox` | 5.0.4 | ~1K ⭐ | Active | Current solution; opaque tokens, not JWT |
| `django-tokenforge` | 1.0.0 | New | Active | Security-first, Knox-like config, replay detection, refresh in HttpOnly cookies |
| `jwtguard` | 0.1.1 | New | Active | Simple, roles support; too immature for production |

**`django-tokenforge`** is the most interesting alternative. It was designed as a "security-first drop-in replacement for `django-rest-knox` when you need stateless access tokens and proper refresh token rotation." [Source](https://pypi.org/project/django-tokenforge/) Key features:
- Stateless HMAC-SHA256 access tokens (zero DB queries per request)
- Refresh token rotation with replay detection (reusing a revoked token revokes the entire family)
- HttpOnly cookie for refresh tokens (not returned in response body)
- Knox-style single `TOKENFORGE = {}` settings dict
- Device fingerprinting (SHA-256 of IP + User-Agent)
- Django signals (`token_rotated`, `token_revoked`, `replay_detected`)
- **Downside:** v1.0.0 is brand new, no community yet, requires Redis for exchange tokens

**`jwtguard`** (v0.1.1) is too immature. "Most JWT libraries for Django are either abandoned, over-engineered, or hide too much behind configuration." While its philosophy is appealing (explicit over magic, role-based permissions), version 0.1.1 with no production track record is disqualifying. [Source](https://pypi.org/project/jwtguard/)

### 3. Best Practices for JWT Auth in Django

Based on SimpleJWT docs and current security consensus:

| Practice | Recommendation | SimpleJWT Setting |
|----------|---------------|-------------------|
| **Short access tokens** | 5–15 minutes | `ACCESS_TOKEN_LIFETIME = timedelta(minutes=5)` (default) |
| **Longer refresh tokens** | 1–30 days | `REFRESH_TOKEN_LIFETIME = timedelta(days=1)` (default) |
| **Refresh token rotation** | **Enable** — issues new refresh token on each refresh | `ROTATE_REFRESH_TOKENS = True` |
| **Blacklist after rotation** | **Enable** — old refresh token is revoked on rotation | `BLACKLIST_AFTER_ROTATION = True` |
| **Token blacklist app** | **Enable** for logout support | Add `'rest_framework_simplejwt.token_blacklist'` to `INSTALLED_APPS` |
| **Dedicated signing key** | Use separate key, not `SECRET_KEY` | `SIGNING_KEY` — "recommended that developers change this setting to a value independent from the django project secret key" [Source](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html) |
| **Expired token cleanup** | Daily cron for `flushexpiredtokens` | Management command provided by blacklist app |
| **Update last_login** | **Disable** (default) — "dramatically increase the number of database transactions" | `UPDATE_LAST_LOGIN = False` |
| **Algorithm** | HS256 (default) for single-service; RS256 for microservices | `ALGORITHM = "HS256"` |
| **Leeway** | 0–30 seconds to account for clock skew | `LEEWAY = 0` (default) |

**Flow:**
1. Client POSTs credentials to `/api/token/` → receives `{access, refresh}`
2. Client sends `Authorization: Bearer <access>` on every request
3. When access expires, client POSTs `{refresh}` to `/api/token/refresh/` → receives new `{access, refresh}` (if rotation enabled)
4. Logout: client POSTs `{refresh}` to `/api/token/blacklist/`

**Verify endpoint:** SimpleJWT also provides `TokenVerifyView` at `/api/token/verify/` — validates a token is cryptographically sound without checking fitness for a specific purpose. Useful for API gateways or microservices that only need to confirm a token hasn't been tampered with. [Source](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html)

**Sliding tokens** are an alternative pattern where a single token serves both purposes and its expiry is extended on each refresh. Not recommended for new projects — the access/refresh pair model with rotation is more secure.

### 4. Migration Guide: django-knox → djangorestframework-simplejwt

There is no official migration guide from Knox to SimpleJWT. The migration is a manual replacement. Here's a step-by-step plan tailored to this project:

#### Step 1: Install SimpleJWT, Remove Knox

```bash
uv add djangorestframework-simplejwt
uv remove django-rest-knox
```

#### Step 2: Update `INSTALLED_APPS`

```python
# Remove: "knox",
# Add:
"rest_framework_simplejwt.token_blacklist",
```

#### Step 3: Replace Authentication Class

```python
# settings.py — REST_FRAMEWORK
# Old:
"DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),

# New:
"DEFAULT_AUTHENTICATION_CLASSES": (
    "rest_framework_simplejwt.authentication.JWTAuthentication",
),
```

#### Step 4: Remove `REST_KNOX` Settings, Add `SIMPLE_JWT` Settings

Replace the entire `REST_KNOX = {...}` block with:

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=10),  # Match old Knox TTL
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("DJANGO_SECRET_KEY"),  # Consider a dedicated key
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
```

#### Step 5: Rewrite Auth Views

The current `LoginView` subclasses `knox.views.LoginView`. This must be rewritten:

**Before (Knox):**
```python
from knox.views import LoginView as KnoxLoginView

class LoginView(KnoxLoginView):
    authentication_classes = (TokenAuthentication,)
    ...
```

**After (SimpleJWT):**
```python
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [UserLoginRateThrottle]
```

**Before (Knox logout):**
```python
path("logout/", knox_views.LogoutView.as_view(), ...)
path("logoutall/", knox_views.LogoutAllView.as_view(), ...)
```

**After (SimpleJWT logout/blacklist):**
```python
path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
```
Knox's `LogoutAllView` has no direct SimpleJWT equivalent — you'd need a custom view that blacklists all outstanding tokens for the user.

#### Step 6: Rewrite Auth Serializer

The `AuthTokenSerializer` must be replaced with a custom `TokenObtainPairSerializer`:

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer that includes user data in the login response."""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Include user info in response (like Knox did)
        data["user"] = UserProfileSerializer(self.user).data
        return data
```

With `ROTATE_REFRESH_TOKENS=True`, the refresh endpoint also needs a custom serializer if you want user data on refresh:

```python
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # data already contains {"access": "..."} and optionally {"refresh": "..."}
        # Add user data if needed
        return data
```

#### Step 7: Update URLs

```python
# apps/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from .views import CreateUserView, LoginView, UserProfileView

app_name = "users"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
]
```

#### Step 8: Run Migrations

```bash
docker compose exec backend python manage.py migrate
```

The `token_blacklist` app creates `OutstandingToken` and `BlacklistedToken` tables.

#### Step 9: Remove Knox User References

Search the codebase for any remaining Knox imports (`from knox...`) and API test assertions that reference Knox token formats. In `conf/test_settings.py`, remove any Knox-specific overrides.

### 5. Token Prefix: "Token" vs "Bearer"

**This project already uses `Bearer` in Knox.** The current `REST_KNOX` config has:

```python
"AUTH_HEADER_PREFIX": "Bearer",
```

Knox's default is `"Token"`, but this project overrode it to `"Bearer"`. SimpleJWT defaults to `("Bearer",)` via `AUTH_HEADER_TYPES`.

**No change needed for existing API clients.** Both the old Knox setup and the new SimpleJWT setup accept `Authorization: Bearer <token>`. [Source](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html)

SimpleJWT's `AUTH_HEADER_TYPES` accepts a tuple — you can support multiple prefixes: `("Bearer", "JWT")` if needed for backward compatibility during migration. The `AUTH_HEADER_NAME` defaults to `"HTTP_AUTHORIZATION"`.

### 6. Settings Reference for Token Lifetime, Refresh, etc.

Complete SimpleJWT settings with defaults and recommendations for this project:

```python
from datetime import timedelta

SIMPLE_JWT = {
    # ── Token Lifetimes ──────────────────────────────────────────
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=10),  # Match Knox 10-hour TTL
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),   # Not used unless sliding tokens
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # ── Rotation & Blacklisting ──────────────────────────────────
    "ROTATE_REFRESH_TOKENS": True,              # REQUIRED for security
    "BLACKLIST_AFTER_ROTATION": True,           # REQUIRED for security
    "UPDATE_LAST_LOGIN": False,                 # Keep False — DB overhead

    # ── Cryptography ─────────────────────────────────────────────
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("DJANGO_SECRET_KEY"),    # ⚠️ Consider dedicated key
    "VERIFYING_KEY": "",                        # Only for asymmetric (RS256)
    "LEEWAY": 0,                                # Seconds of clock skew tolerance

    # ── Headers ──────────────────────────────────────────────────
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    # ── User Identification ──────────────────────────────────────
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    # ── Token Classes ────────────────────────────────────────────
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # ── Custom Serializers ───────────────────────────────────────
    "TOKEN_OBTAIN_SERIALIZER": "apps.users.serializers.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",

    # ── Revocation via password change ───────────────────────────
    "CHECK_REVOKE_TOKEN": False,
    "REVOKE_TOKEN_CLAIM": "hash_password",

    # ── Audience / Issuer (for microservices) ────────────────────
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
}
```

**Key decisions for this project:**
- `ACCESS_TOKEN_LIFETIME = 15 minutes` — standard for SPAs and mobile apps
- `REFRESH_TOKEN_LIFETIME = 10 hours` — matches old Knox `TOKEN_TTL`. Adjust based on security requirements.
- `ROTATE_REFRESH_TOKENS = True` + `BLACKLIST_AFTER_ROTATION = True` — these are the most important security settings. Without them, a stolen refresh token is usable indefinitely.
- `CHECK_REVOKE_TOKEN = False` — when `True`, password changes invalidate all tokens (uses MD5 hash of password). Can be enabled later.

### 7. API Contract Changes

This is the **breaking change** that requires frontend/client updates:

| Aspect | Knox (Current) | SimpleJWT (New) |
|--------|---------------|-----------------|
| **Login endpoint** | `POST /api/v1/auth/login/` | `POST /api/v1/auth/login/` (same URL, different response) |
| **Login request body** | `{email, password}` | `{email, password}` (same — but field name configurable) |
| **Login response** | `{expiry, token, user}` | `{access, refresh}` (no `user` unless custom serializer added) |
| **Token format** | Opaque 64-char hex string | Base64-encoded JWT (3 segments: header.payload.signature) |
| **Auth header** | `Bearer <opaque_token>` | `Bearer <jwt_token>` |
| **Token refresh** | Not used (Knox had auto-refresh option) | `POST .../token/refresh/` with `{refresh}` body |
| **Refresh response** | N/A | `{access, refresh}` (with rotation) |
| **Logout** | `POST .../logout/` — deletes Knox token from DB | `POST .../logout/` — POSTs `{refresh}` to blacklist |
| **Logout all** | `POST .../logoutall/` — deletes all user tokens | No built-in equivalent; needs custom view |

**To maintain backward compatibility**, you can customize the login response:

```python
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["expiry"] = (
            timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME
        ).isoformat()
        data["token"] = data.pop("access")
        data["user"] = UserProfileSerializer(self.user).data
        # Keep "refresh" in the response for the new flow
        return data
```

This would produce: `{expiry, token, refresh, user}` — a superset of both APIs. New clients use `refresh`, old clients ignore it. Old clients still get `token` and `expiry` fields they expect.

**⚠️ Critical caveat:** The old `token` was an opaque string that clients stored and reused. The new `token` (access token) **expires in 15 minutes**. Old clients will break unless they implement the refresh flow, even if the response format looks the same. There is no way around this — JWT access tokens are short-lived by design.

**Migration strategy options:**

1. **Hard cutover** — announce a breaking change, update all clients simultaneously. Simplest if you control all API consumers.
2. **Dual-auth window** — run both Knox and SimpleJWT authentication classes during a transition period. Knox's `TokenAuthentication` raises exceptions on invalid tokens, which blocks fallback. You'd need a custom authentication class that tries JWTAuthentication first, then falls back to a lenient Knox check. This is complex.
3. **Response shim** — use the custom serializer above to return an extended response. Accept that old clients using only `token`/`expiry` have a 15-minute window before they must re-login until they implement refresh.

**Recommendation:** For this starter template (not a production service with existing clients), option 1 (hard cutover) is appropriate. The template's frontend is not included, so API consumers are expected to follow the new contract.

---

## Sources

### Kept
- **Simple JWT Official Docs (Settings)** — https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html — Complete reference for all `SIMPLE_JWT` settings
- **Simple JWT Official Docs (Blacklist App)** — https://django-rest-framework-simplejwt.readthedocs.io/en/stable/blacklist_app.html — Token blacklisting for logout
- **Simple JWT Official Docs (Getting Started)** — https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html — Installation and basic usage
- **Simple JWT settings.py (source)** — https://github.com/jazzband/djangorestframework-simplejwt/blob/master/rest_framework_simplejwt/settings.py — All defaults with types
- **Simple JWT Customizing Token Claims** — https://django-rest-framework-simplejwt.readthedocs.io/en/stable/customizing_token_claims.html — How to add user data to token/response
- **Knox Settings Docs** — https://github.com/jazzband/django-rest-knox/blob/develop/docs/settings.md — Knox settings reference for comparison
- **Knox Auth Docs** — https://jazzband.github.io/django-rest-knox/auth/ — Knox authentication header format
- **django-tokenforge (PyPI)** — https://pypi.org/project/django-tokenforge/ — Most credible alternative, security-first design
- **jwtguard (PyPI)** — https://pypi.org/project/jwtguard/ — New alternative, too immature
- **Simple JWT GitHub** — https://github.com/jazzband/django-rest-framework-simplejwt — 4.3K stars, active in 2026
- **Simple JWT on PyPI** — https://pypi.org/project/djangorestframework-simplejwt/ — ~7M monthly downloads
- **Snyk security score** — https://security.snyk.io/package/pip/djangorestframework-simplejwt — 82/100, no known vulnerabilities
- **dj-rest-auth Upgrade Guide** — https://dj-rest-auth.readthedocs.io/en/latest/reference/upgrade/ — Migration patterns from old JWT libraries
- **DRF Authentication Docs** — https://www.django-rest-framework.org/api-guide/authentication/ — DRF authentication architecture
- **Knox → TokenAuth migration issue** — https://github.com/jazzband/django-rest-knox/issues/220 — Confirms Knox raises exceptions (doesn't return None), complicating dual-auth windows

### Dropped
- **cloudfullstack.dev tutorial** — Blog post, not authoritative
- **studyzone4u.com tutorial** — Blog post, redundant
- **Djamware blog** — General overview, not specific
- **Python in Plain English blog** — General overview, not deep enough
- **Various Stack Overflow answers** — Used one for custom serializer pattern, dropped the rest as redundant with official docs

---

## Gaps

1. **Knox `LogoutAllView` equivalent** — SimpleJWT has no built-in "logout from all devices" endpoint. A custom view would need to query the `OutstandingToken` model and blacklist all tokens for the authenticated user. This is a feature gap that needs custom implementation.

2. **Knox `AUTO_REFRESH` behavior** — Knox can auto-refresh token TTL on each request. SimpleJWT has no equivalent; the client explicitly calls the refresh endpoint. This is a fundamental architectural difference between opaque tokens (extendable TTL) and JWTs (fixed expiry in claims).

3. **Dedicated signing key best practice** — The docs recommend a separate `SIGNING_KEY` from `SECRET_KEY`, but don't provide guidance on key rotation. For a starter template, using `SECRET_KEY` is acceptable; for production, investigate key rotation patterns.

4. **Performance impact of `token_blacklist` app** — The blacklist app adds a DB lookup for every refresh token validation. For very high-traffic APIs, this could be a bottleneck. Redis-backed blacklisting is not built into SimpleJWT (but `django-tokenforge` uses Redis for this).

5. **Test migration effort** — The project's test suite has Knox-specific tests (login response format, token authentication assertions). The full scope of test changes wasn't audited. The test settings file (`conf/test_settings.py`) may have Knox-specific overrides.
