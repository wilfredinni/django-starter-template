# Code Context: Django Knox Auth Exploration

## Files Retrieved

### Core Auth Configuration
1. `conf/settings.py` (lines 78-97, 118-155) — REST_KNOX config, REST_FRAMEWORK auth classes, throttle rates
2. `conf/test_settings.py` (lines 1-18) — Test overrides: Knox ensured installed, request ID middleware mocked, login throttle relaxed
3. `conf/urls.py` (lines 27-42) — API v1 routing: `/api/v1/auth/` → users.urls, `/api/v1/core/` → core.urls
4. `pyproject.toml` (lines 16-17) — Dependency: `django-rest-knox>=5.0.2`, no JWT libraries

### Users App (apps/users/)
5. `apps/users/urls.py` (all 15 lines) — URL patterns: create, profile, login (custom), logout/logoutall (Knox built-in)
6. `apps/users/views.py` (all 70 lines) — Three views: `LoginView` (extends KnoxLoginView), `UserProfileView` (RetrieveUpdateAPIView), `CreateUserView` (CreateAPIView, admin-only)
7. `apps/users/serializers.py` (all 118 lines) — `AuthTokenSerializer`, `CreateUserSerializer`, `UserProfileSerializer`, `LoginResponseSerializer`
8. `apps/users/models.py` (all 30 lines) — `CustomUser(AbstractUser)`: username=None, USERNAME_FIELD='email'
9. `apps/users/managers.py` (all 42 lines) — `CustomUserManager`: email-based user/superuser creation
10. `apps/users/admin.py` (all 37 lines) — `CustomUserAdmin`: email-focused admin panel
11. `apps/users/schema.py` (all 111 lines) — DRF Spectacular OpenAPI response schemas for login, create, profile endpoints
12. `apps/users/throttles.py` (all 30 lines) — `UserLoginRateThrottle`: rate-limit login by IP (anon) or user ID (auth'd)
13. `apps/users/utils.py` (all 15 lines) — `get_errors()`: extracts error messages from ValidationError
14. `apps/users/forms.py` (all 14 lines) — Django admin forms for CustomUser
15. `apps/users/migrations/0001_initial.py` (all 114 lines) — Initial CustomUser migration

### Users Tests
16. `apps/users/tests/test_login_view.py` (all 201 lines) — Login success, invalid creds, inactive user, missing fields, throttling, concurrent tokens
17. `apps/users/tests/test_create_user_view.py` (all 115 lines) — Create user success, password mismatch, weak passwords, duplicates, admin-only, missing fields
18. `apps/users/tests/test_profile_view.py` (all 150 lines) — GET/PUT/PATCH profile, password validation, unauthorized access
19. `apps/users/tests/test_user_model.py` (all 77 lines) — User creation, email normalization, uniqueness, superuser, str representation

### Core App
20. `apps/core/views.py` (all 44 lines) — `ping` (unauthenticated), `fire_task` (deprecated)
21. `apps/core/urls.py` (all 10 lines) — `/api/v1/core/ping/`, `/api/v1/core/fire-task/`
22. `apps/core/schema.py` (all 27 lines) — `ErrorResponseSerializer`, `UNAUTHORIZED_EXAMPLES`
23. `apps/core/tests/test_core_views.py` (all 29 lines) — Ping endpoint tests (no auth needed)
24. `apps/core/management/commands/seed.py` (all 55 lines) — Seeds users + superuser (admin@admin.com / admin)
25. `apps/core/middleware.py` (all 80 lines) — RequestIDMiddleware, request logging context vars
26. `conf/test_utils.py` (all 17 lines) — Mock middleware and log filter for test settings

### Documentation
27. `docs/authentication.md` (all ~185 lines) — Full auth system docs (settings, endpoints, examples)
28. `docs/settings.md` (all ~280 lines) — Comprehensive settings docs covering REST_KNOX, REST_FRAMEWORK, CORS, security
29. `docs/rate_limiting.md` (all ~105 lines) — Throttle configuration and custom throttle docs
30. `docs/testing.md` (all consolidated) — Test patterns, pytest config (note: `addopts` in docs is stale per AGENTS.md)

### Infrastructure
31. `docker-compose.yml` (all 97 lines) — Postgres 18-alpine, Redis 8-alpine, Django + Celery worker + beat
32. `Dockerfile` (all 41 lines) — Python 3.14, multi-stage uv install, appuser
33. `Makefile` (all 77 lines) — `make seed` creates superuser; `make superuser` runs createsuperuser; `make test`
34. `.github/workflows/test.yml` (all 73 lines) — CI: Postgres + Redis services, Python 3.14, `pytest`

### Templates/Frontend
35. `templates/index.html` (all 55 lines) — Landing page with link to admin login (`{% url 'admin:index' %}`); no client-side token handling
36. `static/` — Only contains logo.png, TODO.png, USE.png; no JS/CSS for auth

---

## Key Code

### Knox Settings (`conf/settings.py` lines 118-133)
```python
REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "hashlib.sha512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "apps.users.serializers.UserProfileSerializer",
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "AUTO_REFRESH_MAX_TTL": None,
    "MIN_REFRESH_INTERVAL": 60,
    "AUTH_HEADER_PREFIX": "Bearer",
    "TOKEN_MODEL": "knox.AuthToken",
}
```

### DRF Auth Config (`conf/settings.py` lines 135-153)
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "DEFAULT_THROTTLE_RATES": {
        "user": "1000/day",
        "anon": "100/day",
        "user_login": "5/minute",
    },
}
# In DEBUG mode, SessionAuthentication + BasicAuthentication also enabled
```

### Auth URLs (`apps/users/urls.py`)
```python
urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
```
Mounted at `/api/v1/auth/` via `conf/urls.py`.

### Login View (`apps/users/views.py`)
- Custom `LoginView` extends `KnoxLoginView`
- Uses `AuthTokenSerializer` for validation
- Calls Django `login(request, user)` after Knox auth
- Throttled via `UserLoginRateThrottle` (5/min in production, 1000/min in test)
- Returns: `{ expiry, token, user }` (via `LoginResponseSerializer`)

### User Model (`apps/users/models.py`)
- `CustomUser(AbstractUser)` — `username = None`, `USERNAME_FIELD = "email"`
- Uses `CustomUserManager` — `create_user(email, password)` / `create_superuser(email, password)`
- Migration: `apps/users/migrations/0001_initial.py`

### AuthTokenSerializer (`apps/users/serializers.py` lines 17-41)
- Validates email + password via Django `authenticate()`
- Returns `{ email, password, token }` — token is read_only
- Raises ValidationError on failure (logs warning)

### CreateUserSerializer (`apps/users/serializers.py` lines 44-75)
- Requires email, password, password2, enforces password match
- Password validation with Django validators (minimum length, common, numeric, similarity)
- `CreateUserView` has `permission_classes = (permissions.IsAdminUser,)` — only admins can create users

### UserProfileSerializer (`apps/users/serializers.py` lines 78-106)
- Fields: email, password, first_name, last_name
- Update method handles `set_password()` separately

### Test Overrides (`conf/test_settings.py`)
- Swaps `RequestIDMiddleware`/`RequestIDFilter` with mocks from `conf/test_utils`
- Relaxes login throttle to `1000/minute`

---

## Architecture

### Auth Flow
1. **Login**: POST `/api/v1/auth/login/` with `{email, password}` → `LoginView.post()` validates via `AuthTokenSerializer` → Django `authenticate()` → `login(request, user)` → Knox generates SHA512 token (64 chars, 10hr TTL) → returns `{ expiry, token, user }`
2. **Authenticated Requests**: Client sends `Authorization: Token <token>` → `knox.auth.TokenAuthentication` validates → `request.user` set
3. **Logout**: POST `/api/v1/auth/logout/` → Knox `LogoutView` deletes current token (204)
4. **Logout All**: POST `/api/v1/auth/logoutall/` → Knox `LogoutAllView` deletes all user tokens (204)
5. **Profile**: GET/PUT/PATCH `/api/v1/auth/profile/` → authenticated user only → `UserProfileView`

### Permission Model
- `CreateUserView`: `IsAdminUser` — superuser/admin required to create users
- `UserProfileView`: `IsAuthenticated` — any valid token
- `LoginView`: `AllowAny` — unauthenticated access allowed
- `LogoutView`/`LogoutAllView` (Knox built-in): `IsAuthenticated`

### Throttling
- Login: `UserLoginRateThrottle` (5/min) — identifies by user PK (auth'd) or IP (anon)
- Profile + Create User: `throttling.UserRateThrottle` (1000/day)
- Ping: `PingRateThrottle` (AnonRateThrottle, 10/min)

### Dependencies
- `django-rest-knox>=5.0.2` — the ONLY token library; NO JWT dependencies
- `djangorestframework>=3.15.2`
- `django-cors-headers>=4.5.0`
- `drf-spectacular>=0.29.0` — OpenAPI schema

### No Frontend Auth Code
- No JS/TS files, no Vue/React/Svelte components, no client-side auth handling
- Templates: only `templates/index.html` (landing page with link to admin login)
- Site directory: built mkdocs docs, no application frontend

---

## Start Here
Open `apps/users/views.py` — it's the central auth file containing the custom `LoginView` that extends Knox, plus `CreateUserView` and `UserProfileView`. Then read `apps/users/serializers.py` for the serializers used by those views. The Knox configuration lives in `conf/settings.py` lines 118-155.

## Complete File Index (every file touching auth/knox/token)

| File | Relevance |
|------|-----------|
| `conf/settings.py` | REST_KNOX config, DRF auth classes, throttle rates, AUTH_USER_MODEL, PASSWORD_HASHERS, validators |
| `conf/test_settings.py` | Knox test overrides, mocked middleware, relaxed throttling |
| `conf/urls.py` | API routing: `/api/v1/auth/` → users.urls |
| `pyproject.toml` | `django-rest-knox>=5.0.2` dependency |
| `apps/users/urls.py` | Auth URL patterns (create, profile, login, logout, logoutall) |
| `apps/users/views.py` | LoginView (extends Knox), CreateUserView, UserProfileView |
| `apps/users/serializers.py` | AuthTokenSerializer, CreateUserSerializer, UserProfileSerializer, LoginResponseSerializer |
| `apps/users/models.py` | CustomUser (AbstractUser, email-based) |
| `apps/users/managers.py` | CustomUserManager (create_user, create_superuser) |
| `apps/users/admin.py` | CustomUserAdmin registration |
| `apps/users/schema.py` | OpenAPI response schemas for all auth endpoints |
| `apps/users/throttles.py` | UserLoginRateThrottle |
| `apps/users/utils.py` | get_errors helper |
| `apps/users/forms.py` | Django admin forms |
| `apps/users/migrations/0001_initial.py` | Initial CustomUser migration |
| `apps/users/tests/test_login_view.py` | Login tests (success, invalid, inactive, throttling, concurrent) |
| `apps/users/tests/test_create_user_view.py` | User creation tests (admin-only, validation, duplicates) |
| `apps/users/tests/test_profile_view.py` | Profile CRUD tests, password validation |
| `apps/users/tests/test_user_model.py` | Model unit tests (creation, normalization, uniqueness) |
| `apps/core/schema.py` | ErrorResponseSerializer, UNAUTHORIZED_EXAMPLES |
| `apps/core/middleware.py` | RequestIDMiddleware sets user_id in context vars |
| `apps/core/management/commands/seed.py` | Seed command creates superuser (admin@admin.com/admin) |
| `conf/test_utils.py` | Mock middleware/filter for test settings |
| `docker-compose.yml` | Service definitions |
| `Dockerfile` | Container build |
| `Makefile` | `make seed`, `make superuser`, `make test` |
| `.github/workflows/test.yml` | CI pipeline |
| `.env.example` | Environment variable template |
| `pytest.ini` | Test settings module |
| `templates/index.html` | Landing page (links to admin) |
| `docs/authentication.md` | Auth docs |
| `docs/settings.md` | Settings docs with Knox/REST_FRAMEWORK details |
| `docs/rate_limiting.md` | Throttle docs |
| `docs/testing.md` | Testing docs |
| `AGENTS.md` | AI agent instructions |
