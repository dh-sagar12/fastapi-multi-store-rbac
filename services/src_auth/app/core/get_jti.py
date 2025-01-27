import base64
import hashlib
import secrets
import time
import uuid


def get_jti(length=32):
    random_bytes = secrets.token_bytes(length)
    uuid_bytes = uuid.uuid4().bytes
    timestamp = int(time.time() * 1000).to_bytes(8, "big")
    combined = bytearray()
    combined.extend(random_bytes)
    combined.extend(uuid_bytes)
    combined.extend(timestamp)
    combined.extend(secrets.token_bytes(8))
    final_bytes = hashlib.sha256(combined).digest()
    jti = base64.urlsafe_b64encode(final_bytes).decode("utf-8").rstrip("=")

    return jti
