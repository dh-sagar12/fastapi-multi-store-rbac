import bcrypt


def hash_password(password: str):
    """Transfrom and return plain text password into hashed password."""

    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed_pwd.decode("utf-8")
