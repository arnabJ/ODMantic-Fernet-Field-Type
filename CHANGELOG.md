# Changelog
## 0.0.4 (2025-06-10)

### Added
- EncryptedDecimal Data type
- Custom encoder and parser to BaseEncryptedJSON for successfully Encrypting/Decrypting datetime objects - [@withsmilo](https://github.com/withsmilo)

### Fixed
- EncryptedJSON fails when the dict has a datetime object in any field value. [Fix by [@withsmilo](https://github.com/withsmilo)]

### Updated
- README.md: Added example of the newly added field type
- Fixed Docstring for EncryptedFloat field type
---
## 0.0.3 (2025-03-28)

### Added
- EncryptedInt Data type
- EncryptedFloat Data type
- EncryptedJSON Data type
- Docstrings for all the 4 Field Types

### Updated
- README.md: Added example of the newly added field types

### Cleaned
- Removed unused code from BaseEncryptedString class
---
## 0.0.2 (2025-03-24)

### Added
- Key rotation: Add comma separated multiple keys as the env variable value to use the 1st key for encrypting new data or while updating an existing data and use all the keys for decrypting thus supporting previously encrypted values.

### Fixed
- Fernet key generation command (`fernet-key`) gives `ModuleNotFoundError`.
---
## 0.0.1 (2025-03-23)

### Added
- Initial release of EncryptedString field type
- Utility for generating Fernet key

### Compatibility
- Tested with FastAPI (0.115.11)
- Tested with starlette-admin (0.15.0rc9)
