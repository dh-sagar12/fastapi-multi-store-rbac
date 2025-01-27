import bcrypt


def verify_password(password: str, hashed_password: str):
    """Check if provided password matches with saved password hash."""

    return bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )
