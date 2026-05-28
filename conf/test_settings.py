from .settings import *  # noqa

# Ensure SimpleJWT is properly configured for tests
if "rest_framework_simplejwt" not in INSTALLED_APPS:  # noqa
    INSTALLED_APPS += [
        "rest_framework_simplejwt",
        "rest_framework_simplejwt.token_blacklist",
    ]  # noqa
if "django.middleware.common.CommonMiddleware" in MIDDLEWARE:  # noqa
    index = MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1  # noqa
    MIDDLEWARE.insert(index, "conf.test_utils.RequestIDMiddleware")  # noqa
else:
    MIDDLEWARE.append("conf.test_utils.RequestIDMiddleware")  # noqa

# Test-specific logging configuration
LOGGING["filters"]["request_id"]["()"] = "conf.test_utils.RequestIDFilter"  # noqa
LOGGING["handlers"]["console"]["filters"] = []  # noqa
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa

# Relax throttling for tests
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_login"] = "1000/minute"  # noqa
