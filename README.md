# ODMantic Fernet Field Type

[![Publish Python Package](https://github.com/arnabJ/ODMantic-Fernet-Field-Type/actions/workflows/publish.yml/badge.svg)](https://github.com/arnabJ/ODMantic-Fernet-Field-Type/actions/workflows/publish.yml)
![python-3.8-3.9-3.10-3.11-3.12-3.13](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-informational.svg)
[![Package version](https://img.shields.io/pypi/v/odmantic-fernet-field-type?color=%2334D058&label=pypi)](https://pypi.org/project/odmantic-fernet-field-type)
[![PyPI Downloads](https://static.pepy.tech/badge/odmantic-fernet-field-type)](https://pepy.tech/projects/odmantic-fernet-field-type)

---

A field type that encrypts values using Fernet symmetric encryption.

## Features

- `EncryptedString`: A custom field type that transparently encrypts data before storing it in MongoDB and decrypts it when retrieved
- `EncryptedInt`: A custom field type to encrypt Integer values.
- `EncryptedFloat`: A custom field type to encrypt Floats values.
- `EncryptedJSON`: A custom field type to encrypt JSONs.
- Simple integration with ODMantic models
- Compatible with FastAPI and starlette-admin
- Keys rotation is possible by providing multiple comma separated keys in the env variable.

## Installation

```bash
pip install odmantic-fernet-field-type
```

## Quick Start

### 1. Set up your encryption key

This package requires a Fernet encryption key stored in the `FERNET_KEY` environment variable. You can generate a suitable key by running:

```bash
python -m pip install odmantic-fernet-field-type
fernet-key
```

This will output a generated key along with instructions for setting up your environment.

### 2. Basic Usage

#### Single Key
```dotenv
# .env
...

FERNET_KEY="xxxxxxxyyyyyyyyzzzzzzzzzzz="
```

#### Multiple Keys (For rotation)
```dotenv
# .env
...

FERNET_KEY="pppppppqqqqqqqrrrrrrrrrr=,xxxxxxxyyyyyyyyzzzzzzzzzzz="
```

```python
from odmantic import Model
# Note: The import package is "odmantic_fernet_field" and not "odmantic_fernet_field_type"
from odmantic_fernet_field import EncryptedString, EncryptedInt, EncryptedFloat, EncryptedJSON

class User(Model):
    name: str
    email: str
    password_hash: str
    # This field will be automatically encrypted in the database
    secret_answer: EncryptedString
    account_no: EncryptedInt
    account_balance: EncryptedFloat
    bank_details: EncryptedJSON

...

# Create and save a user - the secret_answer, account_no, account_balance & bank_details will be encrypted in MongoDB
user = User(
    name="John", email="john@example.com", password_hash="...", secret_answer="April 1st, 2025", account_no=1234567890, 
    account_balance=1000000.00, bank_details={
        "accountHolder": "John Doe",
        "accountNumber": 1234567890,
        "type": "Checking",
        "isActive": True
    }
)

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
- Use environment variables
- Rotate your encryption keys periodically [**NEW**]
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
