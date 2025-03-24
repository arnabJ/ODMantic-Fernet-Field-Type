from typing import Annotated, Any

from cryptography.fernet import Fernet, InvalidToken
from odmantic import WithBsonSerializer

from odmantic_fernet_field import get_env_value


class BaseEncryptedString(str):
    """
    A field type that encrypts values using Fernet symmetric encryption.
    Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
    to encrypt the value while all the keys will be used one after the another to try to decode.
    If none of the keys are able to decode, it will raise an exception.

    Example:
        class MyModel(Model):
            secret_data: EncryptedString
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: Any = None):
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            # Fetch the key from env and split it using comma(,)
            fernet_keys = get_env_value("FERNET_KEY").split(",")
            # declare a variable to hold the decrypted value
            decrypted_value = None
            # Loop through each key to try to decrypt
            for key in fernet_keys:
                f = Fernet(key.strip().encode())
                try:
                    decrypted_value = f.decrypt(v).decode()
                    break
                except InvalidToken:
                    pass
            # Return the decrypted value or None if the value didn't decrypt
            return decrypted_value
        if not isinstance(v, str):
            raise TypeError("string required")
        return v


    @WithBsonSerializer
    def __bson__(self, v: str) -> bytes:
        # Fetch the key from env, split it using comma(,) and take the 1st key for encryption
        fernet_key = get_env_value("FERNET_KEY").split(",")[0].encode()
        f = Fernet(fernet_key)
        return f.encrypt(v.encode())


def encrypt_str(v: str) -> bytes:
    # Fetch the key from env, split it using comma(,) and take the 1st key for encryption
    fernet_key = get_env_value("FERNET_KEY").split(",")[0].strip().encode()
    f = Fernet(fernet_key)
    return f.encrypt(v.encode())


EncryptedString = Annotated[BaseEncryptedString, WithBsonSerializer(encrypt_str)]
