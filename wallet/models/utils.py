import string
import secrets

__all__ = ("generate_random_id", "generate_wallet_id")


def generate_random_id(length=12):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def generate_wallet_id():
    return generate_random_id(length=100)
