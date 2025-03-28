import json
from typing import Annotated, Any

from cryptography.fernet import Fernet, InvalidToken
from odmantic import WithBsonSerializer

from odmantic_fernet_field import get_env_value


class BaseEncryptedString(str):
    """
        A field type that encrypts string values using Fernet symmetric encryption.
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
    def validate(cls, v, _: Any = None) -> str:
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


class BaseEncryptedInt(int):
    """
        A field type that encrypts integer values using Fernet symmetric encryption.
        Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
        to encrypt the value while all the keys will be used one after the another to try to decode.
        If none of the keys are able to decode, it will raise an exception.

        Example:
            class MyModel(Model):
                account_number: EncryptedInt
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: Any = None) -> int:
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            # Fetch the key from env and split it using comma(,)
            fernet_keys = get_env_value("FERNET_KEY").split(",")
            # declare a variable to hold the decrypted value
            decrypted_value = None
            # Loop through each key to try to decrypt
            for key in fernet_keys:
                f = Fernet(key.strip().encode())
                try:
                    decrypted_value = int(f.decrypt(v).decode())
                    break
                except InvalidToken:
                    pass
            # Return the decrypted value or None if the value didn't decrypt
            return decrypted_value
        if not isinstance(v, int):
            raise TypeError("int required")
        return v


class BaseEncryptedFloat(float):
    """
        A field type that encrypts float values using Fernet symmetric encryption.
        Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
        to encrypt the value while all the keys will be used one after the another to try to decode.
        If none of the keys are able to decode, it will raise an exception.

        Example:
            class MyModel(Model):
                secret_pricing: EncryptedInt
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: Any = None) -> float:
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            # Fetch the key from env and split it using comma(,)
            fernet_keys = get_env_value("FERNET_KEY").split(",")
            # declare a variable to hold the decrypted value
            decrypted_value = None
            # Loop through each key to try to decrypt
            for key in fernet_keys:
                f = Fernet(key.strip().encode())
                try:
                    decrypted_value = float(f.decrypt(v).decode())
                    break
                except InvalidToken:
                    pass
            # Return the decrypted value or None if the value didn't decrypt
            return decrypted_value
        if not isinstance(v, float):
            raise TypeError("float required")
        return v


class BaseEncryptedJSON(dict):
    """
        A field type that encrypts dict/json values using Fernet symmetric encryption.
        Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
        to encrypt the value while all the keys will be used one after the another to try to decode.
        If none of the keys are able to decode, it will raise an exception.

        Example:
            class MyModel(Model):
                bank_details: EncryptedJSON
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _: Any = None) -> dict:
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            # Fetch the key from env and split it using comma(,)
            fernet_keys = get_env_value("FERNET_KEY").split(",")
            # declare a variable to hold the decrypted value
            decrypted_value = None
            # Loop through each key to try to decrypt
            for key in fernet_keys:
                f = Fernet(key.strip().encode())
                try:
                    decrypted_value = json.loads(f.decrypt(v).decode())
                    break
                except InvalidToken:
                    pass
            # Return the decrypted value or None if the value didn't decrypt
            return decrypted_value
        if not isinstance(v, dict):
            raise TypeError("dict required")
        return v


def encrypt(value: str | int | float | dict) -> bytes:
    """
    Take a string|int|float|dict, and return an encrypted bytes object.

    Args:
        value: plaintext value or JSON to encrypt

    Returns: An encrypted bytes type object.

    """

    # Fetch the key from env, split it using comma(,) and take the 1st key for encryption
    fernet_key = get_env_value("FERNET_KEY").split(",")[0].strip().encode()
    f = Fernet(fernet_key)

    if type(value) is str:
        v = value
    elif type(value) in [int, float]:
        v = str(value)
    elif type(value) is dict:
        v = json.dumps(value)
    else:
        raise TypeError("Only string|int|float|dict supported")

    return f.encrypt(v.encode())


EncryptedString = Annotated[BaseEncryptedString, WithBsonSerializer(encrypt)]
"""
    A custom field type that encrypts string values using Fernet symmetric encryption.
    Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
    to encrypt the value while all the keys will be used one after the another to try to decode.
    If none of the keys are able to decode, it will raise an exception.

    Example:
        class MyModel(Model):
            secret_data: EncryptedString
"""

EncryptedInt = Annotated[BaseEncryptedInt, WithBsonSerializer(encrypt)]
"""
    A custom field type that encrypts int values using Fernet symmetric encryption.
    Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
    to encrypt the value while all the keys will be used one after the another to try to decode.
    If none of the keys are able to decode, it will raise an exception.

    Example:
        class MyModel(Model):
            account_number: EncryptedInt
"""

EncryptedFloat = Annotated[BaseEncryptedFloat, WithBsonSerializer(encrypt)]
"""
    A field type that encrypts float values using Fernet symmetric encryption.
    Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
    to encrypt the value while all the keys will be used one after the another to try to decode.
    If none of the keys are able to decode, it will raise an exception.

    Example:
        class MyModel(Model):
            secret_pricing: EncryptedInt
"""

EncryptedJSON = Annotated[BaseEncryptedJSON, WithBsonSerializer(encrypt)]
"""
    A field type that encrypts dict/json values using Fernet symmetric encryption.
    Keys rotation is possible by providing multiple comma separated keys in the env variable. The 1st key will be used
    to encrypt the value while all the keys will be used one after the another to try to decode.
    If none of the keys are able to decode, it will raise an exception.

    Example:
        class MyModel(Model):
            bank_details: EncryptedJSON
"""
