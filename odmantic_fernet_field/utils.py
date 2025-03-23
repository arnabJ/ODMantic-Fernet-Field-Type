from cryptography.fernet import Fernet


def generate_fernet_key() -> str:
    """
    Generate a new Fernet key suitable for use with FernetField.

    Returns:
        A URL-safe base64-encoded 32-byte key as a string
    """
    return Fernet.generate_key().decode()


def print_key_instructions(key_env_name: str = "FERNET_KEY"):
    """
    Print instructions for setting up the Fernet key.
    """
    key = generate_fernet_key()

    print(f"Generated new Fernet key: {key}")
    print("\nAdd this to your .env file:")
    print(f"{key_env_name}={key}")
    print("\nOr set it as an environment variable:")
    print(f"export {key_env_name}={key}")
    print("\nKeep this key safe and don't lose it, or you won't be able to decrypt your data!")

    return key
