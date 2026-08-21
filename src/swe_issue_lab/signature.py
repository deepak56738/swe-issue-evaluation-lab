"""HMAC helpers used by the webhook verification scenario."""

import hashlib
import hmac


def sign_payload(payload: bytes, secret: bytes) -> str:
    digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(payload: bytes, signature_header: str, secret: bytes) -> bool:
    algorithm, supplied_digest = signature_header.split("=", maxsplit=1)
    if algorithm != "sha256":
        return False
    expected_digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_digest, supplied_digest)
