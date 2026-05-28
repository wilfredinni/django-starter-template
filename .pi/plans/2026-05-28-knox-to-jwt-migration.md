---
title: "Migrate Authentication from django-rest-knox to djangorestframework-simplejwt"
status: done
created: "2026-05-28T19:47:27.118Z"
type: refactor
---

## Overview

Replace `django-rest-knox` token authentication with `djangorestframework-simplejwt` JWT-based authentication. This migrates from opaque 64-char database-backed tokens to stateless JWT access/refresh token pairs.

## ⚠️ Critical Finding: Python 3.14 Compatibility

| Library | Python 3.14 | Django 6.0 |
|---------|------------|------------|
| `django-rest-knox` 5.0.4 | ✅ **Officially supported** (in tox.ini CI) | ✅ |
| `djangorestframework-simplejwt` 5.5.1 | ❌ **Not tested upstream** (max: 3.13 / Django 5.1) | ❌ |

SimpleJWT 5.5.1 **will install** on Python 3.14 (has `>=3.9` constraint), and a community PR (#959) adds Python 3.14/Django 6.0 support but hasn't been merged. The `django.utils.timezone.utc` removal in Django 5.2.7 was fixed in SimpleJWT 5.5.1. **Recommendation**: Run the full test suite as a smoke test in Phase 1 before committing.

Your project uses **Python 3.14** (`.python-version`, Dockerfile) and **Django 6.0**. Knox 5.0.4 explicitly supports both. This migration carries a compatibility risk that must be verified early.

## Current State

### Knox Architecture
- **Package**: `django-rest-knox==5.0.4` (`pyproject.toml:18`)
- **Auth class**: `knox.auth.TokenAuthentication` as default (`conf/settings.py:143`)
- **Login**: Custom `LoginView(KnoxLoginView)` at `apps/users/views.py:25`
- **Logout**: Built-in Knox `LogoutView` / `LogoutAllView` at `apps/users/urls.py:11-13`
- **Serializer**: `AuthTokenSerializer` — email+password → `authenticate()` → returns user, Knox generates token
- **Response**: `{expiry, token, user}` via `LoginResponseSerializer`
- **Token config**: SHA-512, 64-char opaque string, 10hr TTL, `Bearer` prefix, unlimited tokens/user
- **Routes**: `/api/v1/auth/login/`, `/logout/`, `/logoutall/`

### Scout Discovery: Auth Header Bug
Settings say `AUTH_HEADER_PREFIX: "Bearer"` but tests use `Token` prefix:
```python
self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
```
Knox's `TokenAuthentication` defaults to `Token` prefix unless `AUTH_HEADER_PREFIX` is set (which it is to `Bearer`). This discrepancy will be resolved naturally by JWT which uses `Bearer`.

### Current Auth Flow
```
POST /api/v1/auth/login/ {email, password}
  → AuthTokenSerializer.validate() → authenticate(email, password)
  → login(request, user)  # Django session
  → Knox creates AuthToken row, returns {expiry, token, user}

Authenticated request:
  → knox.auth.TokenAuthentication hashes token, looks up in DB, sets request.user

Logout:
  → Deletes AuthToken row from DB
```

## Desired End State

### JWT Architecture
- **Package**: `djangorestframework-simplejwt[crypto]` (HS256 signing)
- **Auth class**: `rest_framework_simplejwt.authentication.JWTAuthentication`
- **Login**: `{access, refresh}` JWT pair — `access` is short-lived, `refresh` is long-lived
- **Refresh**: `TokenRefreshView` — exchanges refresh token for new access token
- **Logout**: `TokenBlacklistView` — adds refresh token to blacklist table
- **Token config**: Access 1hr, Refresh 24hr, HS256, `Bearer` prefix, rotation + blacklist enabled

### New Auth Flow
```
POST /api/v1/auth/login/ {email, password}
  → Returns {access: "<jwt>", refresh: "<jwt>", user: {...}}
  
Authenticated request:
  → JWTAuthentication decodes JWT, extracts user_id, sets request.user
  → No DB lookup needed (stateless)
  
Refresh:
  POST /api/v1/auth/token/refresh/ {refresh: "..."}
  → Returns {access: "<new-jwt>", refresh: "<new-refresh>"}  (when ROTATE_REFRESH_TOKENS=True)
  
Logout:
  POST /api/v1/auth/logout/ {refresh: "..."}
  → Adds refresh token to BlacklistedToken table
```

### Key Differences from Knox

| Feature | Knox | JWT (simplejwt) |
|---------|------|-----------------|
| Token storage | DB table (`knox.AuthToken`) | Stateless (encoded in token itself) |
| Token count | 1 per session | 2 per session (access + refresh) |
| Auth header | `Token <hex>` → `Bearer <hex>` | `Bearer <jwt>` |
| Login response | `{expiry, token, user}` | `{access, refresh, user}` |
| TTL model | Single 10hr token | Access 1hr + Refresh 24hr |
| Logout | Delete from DB | Add to blacklist table |
| Refresh | Auto-refresh (opt-in) | Explicit refresh endpoint |
| LogoutAll | Delete all user tokens | All tokens expire with refresh TTL |

## Out of Scope

- Frontend/client-side changes (JWT storage, refresh interceptor, retry logic)
- Admin panel auth (uses Django sessions, not DRF tokens)
- Rate limiting (existing throttle stays as-is)
- User model changes (CustomUser with email login stays as-is)
- The `login(request, user)` Django session call in LoginView — **needs decision** (see below)

---

## Phase 1: Dependency & Settings (Smoke Test)

### Purpose
Install SimpleJWT, configure settings, and immediately run tests to verify Python 3.14 compatibility.

### Changes
- **`pyproject.toml`**: Remove `django-rest-knox>=5.0.2`, add `djangorestframework-simplejwt[crypto]>=5.4.0`, run `uv lock --upgrade`
- **`conf/settings.py`**:
  - `INSTALLED_APPS`: Replace `"knox"` with `"rest_framework_simplejwt"` + `"rest_framework_simplejwt.token_blacklist"`
  - Remove `REST_KNOX = {...}` block (lines 129-142)
  - Add `SIMPLE_JWT = {...}` configuration
  - `DEFAULT_AUTHENTICATION_CLASSES`: `"knox.auth.TokenAuthentication"` → `"rest_framework_simplejwt.authentication.JWTAuthentication"`
- **`conf/test_settings.py`**: Replace `"knox"` with `"rest_framework_simplejwt"` in INSTALLED_APPS guard

### SIMPLE_JWT Configuration
```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=24),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
```

### Verification (CRITICAL — block on failure)
- [ ] Build: `make rebuild`
- [ ] Migrations: `make migrate` (creates `token_blacklist_outstandingtoken` and `token_blacklist_blacklistedtoken` tables)
- [ ] **Smoke test**: `make test` — does SimpleJWT import without errors?
- [ ] Shell check: `make shell` → `from rest_framework_simplejwt.authentication import JWTAuthentication` succeeds
- [ ] Check for `django.utils.timezone.utc` or other Python 3.14 compat issues

⏸️ **PAUSE — If tests fail with import errors, reassess. If they pass, proceed.** 

---

## Phase 2: Serializers, Views, and URLs

### Changes
- **`apps/users/serializers.py`**:
  - `AuthTokenSerializer`: Remove `token` CharField (JWT generates tokens in the view, not the serializer). Keep email+password validation.
  - `LoginResponseSerializer`: Replace `expiry`, `token` with `access`, `refresh` fields
  - **No custom `TokenObtainPairSerializer` needed**: SimpleJWT auto-detects `USERNAME_FIELD='email'` from CustomUser
- **`apps/users/views.py`**:
  - Remove Knox imports
  - Replace `LoginView(KnoxLoginView)` with custom `LoginView(TokenObtainPairView)`:
    - Keep `AuthTokenSerializer` as `serializer_class`
    - Keep `UserLoginRateThrottle`
    - Keep logging
    - Generate JWT via `RefreshToken.for_user(user)` instead of delegating to Knox
    - **Decision needed**: Keep or drop `login(request, user)` (Django session)
  - Add `LogoutView(APIView)` for blacklist-based logout
  - `UserProfileView` and `CreateUserView` unchanged (use `IsAuthenticated`, not Knox directly)
- **`apps/users/urls.py`**:
  - Replace Knox routes with SimpleJWT routes
  - Rename URL names: `knox_login` → `login`, `knox_logout` → `logout`
  - Add `token/refresh/` and `token/verify/` endpoints
  - Drop `logoutall/` (JWT equivalent: all tokens expire with refresh TTL)
- **`apps/users/schema.py`**:
  - Update `LOGIN_RESPONSE_SCHEMA` for new response shape

### Login View
```python
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    throttle_classes = [UserLoginRateThrottle]

    def post(self, request, format=None) -> Response:
        serializer = AuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)  # Keep for admin panel? TBD
        logger.info("User %s logged in.", user.email)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserProfileSerializer(user).data,
        })
```

### Logout View
```python
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
```

### New URL Structure
```python
urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
```

### Verification
- [ ] Login: `POST /api/v1/auth/login/` returns `{access, refresh, user}` with 200
- [ ] Auth: `GET /api/v1/auth/profile/` with `Authorization: Bearer <access>` returns 200
- [ ] Refresh: `POST /api/v1/auth/token/refresh/` returns new access token
- [ ] Logout: `POST /api/v1/auth/logout/` returns 205, token blacklisted
- [ ] Old `Token` prefix returns 401

⏸️ **PAUSE — Manual smoke test with curl/httpie**

---

## Phase 3: Test Migration

### Changes
- **`apps/users/tests/test_login_view.py`** (7 tests):
  - URL name: `"v1:users:knox_login"` → `"v1:users:login"`
  - `test_login_success`: Assert `"access"`, `"refresh"`, `"user"` (not `"expiry"`, `"token"`)
  - `test_concurrent_login`: `HTTP_AUTHORIZATION=f"Token {token}"` → `f"Bearer {access}"` 
  - `test_concurrent_login`: Generate JWT: `from rest_framework_simplejwt.tokens import RefreshToken; token = RefreshToken.for_user(user)`
  - All 4xx/5xx tests: unchanged
  - `test_login_throttling`: update response field assertions
- **`apps/users/tests/test_profile_view.py`** (9 tests): Uses `force_authenticate()` → **no changes needed**
- **`apps/users/tests/test_create_user_view.py`** (7 tests): Uses `force_authenticate()` → **no changes needed**
- **New: `apps/users/tests/test_token_refresh.py`**:
  - Test refresh with valid refresh token → returns new access
  - Test refresh with expired token → 401
  - Test refresh with blacklisted token → 401
  - Test access token works after refresh rotation

### Verification
- [ ] `docker compose exec backend pytest apps/users/` — all tests pass
- [ ] `make test-cov` — no coverage drop

---

## Phase 4: Cleanup

### Changes
- Remove all Knox references: `grep -r "knox" apps/ conf/` should return only comments
- Update `AGENTS.md`: "Auth: Knox tokens (sha512, 64 chars, 10hr TTL, Token prefix)" → "Auth: JWT tokens (simplejwt, HS256, access 1hr + refresh 24hr, Bearer prefix)"
- Run `uv run ruff check .` and `uv run mypy .`
- Verify `drf-spectacular` Swagger UI shows updated auth endpoints

### Verification
- [ ] `make test` green
- [ ] `uv run ruff check .` clean
- [ ] `uv run mypy .` clean
- [ ] Swagger UI at `/api/schema/swagger-ui/` shows new endpoints

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Python 3.14 incompatibility** | 🔴 **BLOCKING** | Smoke test in Phase 1. If SimpleJWT fails, consider: (a) the unmerged community PR, (b) staying on Knox, or (c) wrapping PyJWT directly |
| Client response format breaks | 🟡 High | Document new `{access, refresh}` shape. Update all clients. |
| Auth header prefix change | 🟡 Medium | Setting `AUTH_HEADER_TYPES: ("Bearer",)` matches Knox's configured `AUTH_HEADER_PREFIX: "Bearer"`. Tests currently use `Token` prefix (bug) — will fix. |
| Existing Knox tokens invalid | 🟢 Low | Accept during deploy. Old tokens in DB become orphaned; drop `knox_authtoken` table after migration. |
| Token blacklist table grows unbounded | 🟢 Low | Add `python manage.py flushexpiredtokens` to daily cron/Celery beat. |
| `login()` session dependency | 🟢 Low | Keep `login(request, user)` — it's harmless for JWT and preserves admin panel session compatibility. |

## Open Questions for User

1. **Django `login()` session**: Keep it for admin panel compat, or drop it since JWT is stateless? (I recommend **keep** — zero downside)
2. **Token TTL**: Access 1hr / Refresh 24hr. Current Knox is single 10hr token. Does this split work?
3. **Backward compat**: Any existing API clients expecting `{expiry, token, user}`? If yes, we need a versioned transition.
4. **URL naming**: Rename `knox_login` to `login` or keep old names?

## References

- [SimpleJWT Getting Started](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [SimpleJWT Settings](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)
- [SimpleJWT Blacklist App](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html)
- [SimpleJWT Serializers Source](https://github.com/jazzband/djangorestframework-simplejwt/blob/master/rest_framework_simplejwt/serializers.py) — auto-detects USERNAME_FIELD
- [Python 3.14 compat PR (unmerged)](https://github.com/bhardwajRahul/django-rest-framework-simplejwt/commit/6a9e048dd92c45a4f6bbe92b9166d658c4024f55)
- [Knox 5.0.4 tox.ini](https://github.com/jazzband/django-rest-knox/blob/develop/tox.ini) — Python 3.14 + Django 6.0 in CI
- [Knox→JWT discussion](https://github.com/jazzband/django-rest-knox/issues/220)
