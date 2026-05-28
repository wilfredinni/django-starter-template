# Authentication System

## Overview

This section provides a comprehensive guide to the authentication system implemented in the Django Starter Template. It covers the core authentication endpoints, security settings, and how JWT-based authentication is managed.

## Authentication Settings

The following settings in `conf/settings.py` are relevant to authentication and user management:

*   `AUTH_USER_MODEL`: Specifies the custom user model to use. **Default:** `users.CustomUser`. This allows you to extend Django's default user model with custom fields and behaviors.

*   `MIN_PASSWORD_LENGTH`: Minimum length for user passwords. **Default:** `8` (loaded from `env.int("MIN_PASSWORD_LENGTH", default=8)`). This is used by the password validation system.

*   `PASSWORD_HASHERS`: A list of password hashing algorithms used for storing user passwords. **Default:** A list including `ScryptPasswordHasher`, `PBKDF2PasswordHasher`, `PBKDF2SHA1PasswordHasher`, `Argon2PasswordHasher`, and `BCryptSHA256PasswordHasher`. This provides strong password security.

*   `AUTH_PASSWORD_VALIDATORS`: Configures password validation rules. **Default:** Includes validators for user attribute similarity, minimum length, common passwords, and numeric passwords. You can customize these to enforce stronger password policies.

### JWT Authentication

The template uses `djangorestframework-simplejwt` for secure, JWT-based (JSON Web Token) authentication. This system provides stateless authentication with access and refresh token pairs. The following settings, configured under `SIMPLE_JWT` in `conf/settings.py`, control its behavior:

*   `ACCESS_TOKEN_LIFETIME`: How long access tokens remain valid before requiring a refresh. **Default:** `timedelta(hours=1)`.
*   `REFRESH_TOKEN_LIFETIME`: How long refresh tokens remain valid before requiring a full re-login. **Default:** `timedelta(hours=24)`.
*   `ROTATE_REFRESH_TOKENS`: Whether a new refresh token is issued on each refresh. **Default:** `True`.
*   `BLACKLIST_AFTER_ROTATION`: Whether old refresh tokens are blacklisted on rotation. **Default:** `True`.
*   `UPDATE_LAST_LOGIN`: Whether `last_login` is updated on authentication. **Default:** `True`.
*   `ALGORITHM`: The signing algorithm for JWTs. **Default:** `"HS256"`.
*   `SIGNING_KEY`: The secret key used to sign tokens. **Default:** Uses `DJANGO_SECRET_KEY`.
*   `AUTH_HEADER_TYPES`: The accepted authorization header prefix. **Default:** `("Bearer",)`.
*   `USER_ID_FIELD`: The model field used to identify users in the JWT payload. **Default:** `"id"`.
*   `USER_ID_CLAIM`: The claim name in the JWT payload for the user ID. **Default:** `"user_id"`.
*   `TOKEN_OBTAIN_SERIALIZER`: Custom serializer for the login endpoint. **Default:** `apps.users.serializers.CustomTokenObtainPairSerializer`, which includes user profile data in the response.

### REST Framework Settings

Django REST Framework (DRF) settings, particularly authentication classes and throttle rates, are configured to manage API access and prevent abuse:

*   `DEFAULT_AUTHENTICATION_CLASSES`: Defines the authentication methods available for API endpoints. **Default:** `rest_framework_simplejwt.authentication.JWTAuthentication`. In `DEBUG` mode, `SessionAuthentication` and `BasicAuthentication` are also enabled for convenience.

*   `DEFAULT_THROTTLE_RATES`: Configures rate limiting to control the number of requests users can make within a given timeframe. **Default:**
    *   `user: "1000/day"` (authenticated users)
    *   `anon: "100/day"` (unauthenticated users)
    *   `user_login: "5/minute"` (specific throttle for login attempts)

These rates can be adjusted in `conf/settings.py` to suit your application's specific needs and security requirements.

## Authentication Endpoints

### Create User

This endpoint allows an admin user to register a new user account.

**Request:**

*   **Method:** `POST`
*   **URL:** `/api/v1/auth/create/`
*   **Authentication:** Admin user required
*   **Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "complexpassword123",
        "password2": "complexpassword123"
    }
    ```
    *   `email`: The user's unique email address.
    *   `password`: The user's chosen password.
    *   `password2`: Confirmation of the user's chosen password (must match `password`).

**Responses:**

*   **Success (201 Created):**
    ```json
    {
        "email": "user@example.com"
    }
    ```
    *   Returns the email of the newly created user.

*   **Error (400 Bad Request):**
    *   **Passwords do not match:**
        ```json
        {
            "non_field_errors": [
                "Passwords do not match."
            ]
        }
        ```
    *   **Email already registered:**
        ```json
        {
            "email": [
                "This email is already registered."
            ]
        }
        ```
    *   **Invalid password (e.g., too short, common password):**
        ```json
        {
            "password": [
                "This password is too short. It must contain at least 8 characters."
            ]
        }
        ```
*   **Error (401 Unauthorized):**
    *   This error occurs if authentication credentials are missing or invalid.
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

### Login

This endpoint authenticates a user and returns a JWT access/refresh token pair.

**Request:**

*   **Method:** `POST`
*   **URL:** `/api/v1/auth/login/`
*   **Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "complexpassword123"
    }
    ```
    *   `email`: The user's registered email address.
    *   `password`: The user's password.

**Responses:**

*   **Success (200 OK):**
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "email": "user@example.com",
            "first_name": "",
            "last_name": ""
        }
    }
    ```
    *   `access`: A short-lived JWT access token (1 hour).
    *   `refresh`: A long-lived JWT refresh token (24 hours).
    *   `user`: A dictionary containing basic user profile information.

*   **Error (401 Unauthorized):**
    *   **Invalid credentials:**
        ```json
        {
            "detail": "No active account found with the given credentials"
        }
        ```
    *   **Missing fields:**
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

### Token Refresh

This endpoint exchanges a valid refresh token for a new access/refresh token pair.

**Request:**

*   **Method:** `POST`
*   **URL:** `/api/v1/auth/token/refresh/`
*   **Body:**
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

**Responses:**

*   **Success (200 OK):**
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    *   Returns new access and refresh tokens. The old refresh token is blacklisted.

*   **Error (401 Unauthorized):**
    ```json
    {
        "detail": "Token is invalid or expired"
    }
    ```

### Token Verify

This endpoint validates whether a token is cryptographically valid.

**Request:**

*   **Method:** `POST`
*   **URL:** `/api/v1/auth/token/verify/`
*   **Body:**
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

**Responses:**

*   **Success (200 OK):**
    *   Empty response body with status 200 indicates the token is valid.

*   **Error (401 Unauthorized):**
    *   The token is invalid, expired, or tampered with.

### Logout

This endpoint blacklists the provided refresh token, preventing future use.

**Request:**

*   **Method:** `POST`
*   **URL:** `/api/v1/auth/logout/`
*   **Body:**
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

**Responses:**

*   **Success (200 OK):**
    *   The refresh token has been blacklisted. The access token will continue to work until it expires naturally (1 hour).

*   **Error (400/401):**
    *   Occurs if the refresh token is missing, invalid, or already blacklisted.

### User Profile

This endpoint allows authenticated users to retrieve and update their profile information.

#### Retrieve User Profile

Retrieves the profile of the currently authenticated user.

**Request:**

*   **Method:** `GET`
*   **URL:** `/api/v1/auth/profile/`
*   **Authentication:** Bearer JWT token required.

**Responses:**

*   **Success (200 OK):**
    ```json
    {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    ```
    *   Returns the user's email, first name, and last name.

*   **Error (401 Unauthorized):**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

#### Update User Profile

Updates the entire profile of the currently authenticated user. All fields must be provided.

**Request:**

*   **Method:** `PUT`
*   **URL:** `/api/v1/auth/profile/`
*   **Authentication:** Bearer JWT token required.
*   **Body:**
    ```json
    {
        "email": "user@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "newpassword123"
    }
    ```

**Responses:**

*   **Success (200 OK):**
    ```json
    {
        "email": "user@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    ```

*   **Error (400 Bad Request):**
    ```json
    {
        "password": [
            "Password must be at least 8 characters long."
        ]
    }
    ```

*   **Error (401 Unauthorized):**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

#### Partially Update User Profile

Partially updates the profile of the currently authenticated user. Only the fields to be updated need to be provided.

**Request:**

*   **Method:** `PATCH`
*   **URL:** `/api/v1/auth/profile/`
*   **Authentication:** Bearer JWT token required.
*   **Body:**
    ```json
    {
        "first_name": "Jane"
    }
    ```

**Responses:**

*   **Success (200 OK):**
    ```json
    {
        "email": "user@example.com",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    ```

*   **Error (401 Unauthorized):**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

## Authentication Flow

1. **Login:** POST `/api/v1/auth/login/` with `{email, password}` → returns `{access, refresh, user}`.
2. **Authenticated Requests:** Send `Authorization: Bearer <access_token>` header on every API request.
3. **Token Refresh:** When the access token expires, POST `/api/v1/auth/token/refresh/` with `{refresh}` to get a new access/refresh pair.
4. **Logout:** POST `/api/v1/auth/logout/` with `{refresh}` to blacklist the refresh token.
5. **Profile:** GET/PUT/PATCH `/api/v1/auth/profile/` with a valid Bearer token.
