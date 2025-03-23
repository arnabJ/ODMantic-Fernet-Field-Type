from typing import Annotated, Any

from cryptography.fernet import Fernet, InvalidToken
from odmantic import WithBsonSerializer

from odmantic_fernet_field import get_env_value


class EncryptedStringBase(str):
    """
    A field type that encrypts values using Fernet symmetric encryption.

    Example:
        class MyModel(Model):
            secret_data: EncryptedString
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info: Any = None):
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            f = Fernet(get_env_value("FERNET_KEY").encode())
            try:
                return f.decrypt(v).decode()
            except InvalidToken:
                return "--failed to decode--"
        if not isinstance(v, str):
            raise TypeError("string required")
        return v


def encrypt_str(v: EncryptedStringBase) -> bytes:
    f = Fernet(get_env_value("FERNET_KEY").encode())
    return f.encrypt(v.encode())


EncryptedString = Annotated[EncryptedStringBase, WithBsonSerializer(encrypt_str)]
