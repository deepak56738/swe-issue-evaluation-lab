from swe_issue_lab.signature import sign_payload, verify_signature


def test_accepts_valid_sha256_signature() -> None:
    payload = b'{"event":"order.created"}'
    secret = b"test-secret"

    signature = sign_payload(payload, secret)

    assert verify_signature(payload, signature, secret) is True


def test_rejects_digest_for_different_payload() -> None:
    secret = b"test-secret"
    signature = sign_payload(b"original", secret)

    assert verify_signature(b"modified", signature, secret) is False


def test_rejects_unsupported_algorithm() -> None:
    assert verify_signature(b"payload", "sha1=abc", b"secret") is False
