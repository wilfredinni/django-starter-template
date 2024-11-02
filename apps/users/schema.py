from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from .serializers import (
    LoginResponseSerializer,
    UserProfileSerializer,
    CreateUserSerializer,
)

ErrorResponseSerializer = inline_serializer(
    name="ErrorResponse",
    fields={
        "detail": serializers.CharField(read_only=True),
    },
)

BAD_CREDENTIALS_EXAMPLE = OpenApiExample(
    "Bad Credentials",
    value={"non_field_errors": ["Unable to log in with provided credentials."]},
    status_codes=["400"],
)

MISSING_FIELDS_EXAMPLE = OpenApiExample(
    "Missing Fields",
    value={
        "email": ["This field is required."],
        "password": ["This field is required."],
    },
    status_codes=["400"],
)

UNAUTHORIZED_EXAMPLES = [
    OpenApiExample(
        "Unauthorized",
        value={"detail": "Authentication credentials were not provided."},
        status_codes=["401"],
    ),
    OpenApiExample(
        "Unauthorized",
        value={"detail": "Invalid token."},
        status_codes=["401"],
    ),
]

LOGIN_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        response=LoginResponseSerializer,
        description="Successful login response",
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Bad request response",
        examples=[BAD_CREDENTIALS_EXAMPLE, MISSING_FIELDS_EXAMPLE],
    ),
}

PROFILE_RESPONSE_SCHEMA = {
    200: OpenApiResponse(
        response=UserProfileSerializer,
        description="User profile response",
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="PUT request with missing fields",
        examples=[
            OpenApiExample(
                "Bad Request",
                value={"password": ["This field is required."]},
                status_codes=["400"],
            )
        ],
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Unauthorized response",
        examples=UNAUTHORIZED_EXAMPLES,
    ),
}

USER_CREATE_RESPONSE_SCHEMA = {
    201: OpenApiResponse(
        response=CreateUserSerializer,
        description="User creation response",
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Bad request response",
        examples=[
            OpenApiExample(
                "Bad Request",
                value={
                    "email": ["This field may not be blank."],
                    "password": ["This field may not be blank."],
                    "password2": ["This field may not be blank."],
                },
                status_codes=["400"],
            ),
        ],
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Unauthorized response",
        examples=UNAUTHORIZED_EXAMPLES,
    ),
}
