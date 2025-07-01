# Authentication Endpoints

This section details the API endpoints related to user authentication and management, all prefixed with `/auth/`.

## Authentication Settings

The following settings in `conf/settings.py` are relevant to authentication and user management:

*   `AUTH_USER_MODEL`: Specifies the custom user model to use. **Default:** `users.CustomUser`. This allows you to extend Django's default user model with custom fields and behaviors.

*   `MIN_PASSWORD_LENGTH`: Minimum length for user passwords. **Default:** `8` (loaded from `env.int("MIN_PASSWORD_LENGTH", default=8)`). This is used by the password validation system.

*   `PASSWORD_HASHERS`: A list of password hashing algorithms used for storing user passwords. **Default:** A list including `ScryptPasswordHasher`, `PBKDF2PasswordHasher`, `PBKDF2SHA1PasswordHasher`, `Argon2PasswordHasher`, and `BCryptSHA256PasswordHasher`. This provides strong password security.

*   `AUTH_PASSWORD_VALIDATORS`: Configures password validation rules. **Default:** Includes validators for user attribute similarity, minimum length, common passwords, and numeric passwords. You can customize these to enforce stronger password policies.

### `REST_KNOX`

Configuration for `django-rest-knox`, the token-based authentication system.

*   `SECURE_HASH_ALGORITHM`: The hashing algorithm used for tokens. **Default:** `hashlib.sha512`.
*   `AUTH_TOKEN_CHARACTER_LENGTH`: The length of the authentication token. **Default:** `64`.
*   `TOKEN_TTL`: Token time-to-live. **Default:** `timedelta(hours=10)`. This defines how long a token is valid.
*   `USER_SERIALIZER`: The serializer used for user profiles. **Default:** `apps.users.serializers.UserProfileSerializer`.
*   `TOKEN_LIMIT_PER_USER`: Limits the number of active tokens per user. **Default:** `None` (no limit).
*   `AUTO_REFRESH`: Whether tokens should be automatically refreshed. **Default:** `False`.
*   `AUTO_REFRESH_MAX_TTL`: Maximum time-to-live for auto-refreshed tokens. **Default:** `None`.
*   `MIN_REFRESH_INTERVAL`: Minimum interval between token refreshes. **Default:** `60` seconds.
*   `AUTH_HEADER_PREFIX`: The prefix for the Authorization header. **Default:** `Bearer`.
*   `TOKEN_MODEL`: The token model used. **Default:** `knox.AuthToken`.

### `REST_FRAMEWORK` Authentication Classes and Throttle Rates

*   `DEFAULT_AUTHENTICATION_CLASSES`: Defines authentication methods. **Default:** `knox.auth.TokenAuthentication`. In `DEBUG` mode, `SessionAuthentication` and `BasicAuthentication` are also added.

*   `DEFAULT_THROTTLE_RATES`: Configures rate limiting for different user types. **Default:** `user: "1000/day"`, `anon: "100/day"`, `user_login: "5/minute"`. These can be adjusted based on your application's needs.

## Endpoints

### Create User

POST /auth/create/

Creates a new user.

**Request Body:**

```json
{
    "email": "user@example.com",
    "password": "complexpassword123",
    "password2": "complexpassword123"
}
```

**Success Response (201 Created):**

```json
{
    "email": "user@example.com"
}
```

**Error Responses:**

**400 Bad Request (Passwords do not match):**

```json
{
    "password": [
        "Passwords do not match."
    ]
}
```

**400 Bad Request (Email already registered):**

```json
{
    "email": [
        "This email is already registered."
    ]
}
```

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Login

POST /auth/login/

Logs in a user and returns an authentication token.

**Request Body:**

```json
{
    "email": "user@example.com",
    "password": "complexpassword123"
}
```

**Success Response (200 OK):**

```json
{
    "expiry": "2025-07-09T12:00:00Z",
    "token": "your-auth-token",
    "user": {
        "email": "user@example.com",
        "first_name": "",
        "last_name": ""
    }
}
```

**Error Responses:**

**400 Bad Request (Invalid credentials):**

```json
{
    "detail": "Unable to log in with provided credentials."
}
```

**400 Bad Request (Missing fields):**

```json
{
    "email": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}
```

### Logout

POST /auth/logout/

Logs out the currently authenticated user.

**Success Response (204 No Content):**

The response will have an empty body.

**Error Responses:**

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Logout All

POST /auth/logoutall/

Logs out the currently authenticated user from all sessions.

**Success Response (204 No Content):**

The response will have an empty body.

**Error Responses:**

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### User Profile

GET /auth/profile/

Retrieves the profile of the currently authenticated user.

**Success Response (200 OK):**

```json
{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Error Responses:**

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

PUT /auth/profile/

Updates the profile of the currently authenticated user.

**Request Body:**

```json
{
    "first_name": "Jane",
    "last_name": "Doe"
}
```

**Success Response (200 OK):**

```json
{
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
}
```

**Error Responses:**

**400 Bad Request (Invalid data):**

```json
{
    "password": [
        "Password must be at least 8 characters long."
    ]
}
```

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```

PATCH /auth/profile/

Partially updates the profile of the currently authenticated user.

**Request Body:**

```json
{
    "first_name": "Jane"
}
```

**Success Response (200 OK):**

```json
{
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe"
}
```

**Error Responses:**

**401 Unauthorized:**

```json
{
    "detail": "Authentication credentials were not provided."
}
```