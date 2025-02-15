from .settings import *  # noqa

# Change the throttle rates for testing
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["user_login"] = "1000/minute"  # noqa
