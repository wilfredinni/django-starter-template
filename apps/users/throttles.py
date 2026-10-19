from collections.abc import Mapping
from hashlib import sha256

from rest_framework.throttling import SimpleRateThrottle


class UserLoginRateThrottle(SimpleRateThrottle):
    """Limit login attempts per IP, even when a token is supplied."""

    scope = "user_login"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class LoginAccountRateThrottle(UserLoginRateThrottle):
    """Limit attempts against an account across source IPs."""

    def get_cache_key(self, request, view):
        if not isinstance(request.data, Mapping):
            return None
        email = request.data.get("email")
        if not isinstance(email, str) or not email.strip():
            return None
        digest = sha256(email.strip().casefold().encode(errors="replace")).hexdigest()
        return self.cache_format % {"scope": self.scope, "ident": f"account_{digest}"}
