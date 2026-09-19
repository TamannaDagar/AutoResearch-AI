import re
import hashlib
import secrets


def validate_email(email: str) -> bool:
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    return (
        len(password) >= 8
        and bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[a-z]", password))
        and bool(re.search(r"[0-9]", password))
        and bool(re.search(r"[^A-Za-z0-9]", password))
    )


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )

    return f"{salt.hex()}:{password_hash.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600_000,
        )

        return secrets.compare_digest(
            password_hash.hex(),
            hash_hex,
        )

    except (ValueError, TypeError):
        return False