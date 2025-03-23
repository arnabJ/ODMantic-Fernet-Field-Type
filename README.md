# ODMantic Fernet Field Type

A specialized encrypted string field type for ODMantic that provides transparent encryption/decryption of string data in MongoDB.

## Features

- `EncryptedString`: A custom field type that transparently encrypts data before storing it in MongoDB and decrypts it when retrieved
- Simple integration with ODMantic models
- Compatible with FastAPI and starlette-admin

## Installation

```bash
pip install odmantic-fernet-field-type
```

## Quick Start

### 1. Setup your encryption key

This package requires a Fernet encryption key stored in the `FERNET_KEY` environment variable. You can generate a suitable key by running:

```bash
python -m pip install odmantic-fernet-field-type
fernet-key
```

This will output a generated key along with instructions for setting up your environment.

### 2. Basic Usage

```python
from odmantic import Model, Field
from odmantic_fernet_field import EncryptedString

class User(Model):
    name: str
    email: str
    password_hash: str
    # This field will be automatically encrypted in the database
    secret_answer: EncryptedString

...

# Create and save a user - the secret_answer will be encrypted in MongoDB
user = User(name="John", email="john@example.com", password_hash="...", secret_answer="April 1st, 2025")

# When you retrieve the user, the secret_answer is automatically decrypted
retrieved_user = await engine.find_one(User, User.email == "john@example.com")
assert retrieved_user.secret_answer == "April 1st, 2025"  # This will pass!
```

### Integration with FastAPI and starlette-admin

The package has been tested and works with FastAPI and starlette-admin:

```python
from fastapi import FastAPI
from starlette_admin import Admin
from starlette_admin.contrib.odmantic import ModelView
from models import User

app = FastAPI()
admin = Admin(title="Admin Panel")

class UserAdmin(ModelView):
    # Configure your admin view
    pass

admin.add_view(UserAdmin(User))
admin.mount_to(app)
```

## Security Considerations

- Never hardcode encryption keys in your source code
- Use environment variables or a secure key management solution
- Rotate your encryption keys periodically [**Coming Soon**]
- Back up your encryption keys - if lost, encrypted data cannot be recovered

## Compatibility

- Python 3.9+
- ODMantic 1.0.2+
- MongoDB 6.0+
- Tested with MongoDB 8.0.5

## Dependencies

- odmantic 1.0.2+
- python-dotenv 1.0.1+
- cryptography 44.0.2+

## Inspiration

This package was inspired by [django-fernet-fields](https://github.com/orcasgit/django-fernet-fields), which provides similar functionality for Django models.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
