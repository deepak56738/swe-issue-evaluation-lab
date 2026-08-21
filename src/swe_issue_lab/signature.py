"""HMAC helpers used by the webhook verification scenario."""

import hashlib
import hmac
import re

SHA256_SIGNATURE = re.compile(r"^sha256=([0-9a-f]{64})$")


def sign_payload(payload: bytes, secret: bytes) -> str:
    digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def verify_signature(payload: bytes, signature_header: str, secret: bytes) -> bool:
    match = SHA256_SIGNATURE.fullmatch(signature_header)
    if match is None:
        return False
    supplied_digest = match.group(1)
    expected_digest = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_digest, supplied_digest)
