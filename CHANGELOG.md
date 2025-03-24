# Changelog

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
