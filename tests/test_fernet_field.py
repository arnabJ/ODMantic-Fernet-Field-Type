import os
import pytest
from unittest.mock import patch, MagicMock
from cryptography.fernet import InvalidToken

import json
from datetime import datetime

from odmantic_fernet_field.fernet_field import (
    BaseEncryptedString,
    BaseEncryptedInt,
    BaseEncryptedFloat,
    BaseEncryptedJSON,
    encrypt,
)


@pytest.fixture(autouse=True)
def set_fernet_key_env():
    os.environ["FERNET_KEY"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa="  # dummy key for testing
    yield
    del os.environ["FERNET_KEY"]


@pytest.fixture
def mock_fernet_decrypt_success():
    with patch("odmantic_fernet_field.fernet_field.Fernet") as MockFernet:
        instance = MockFernet.return_value
        instance.decrypt.side_effect = lambda x: b"decrypted_value"
        yield MockFernet


@pytest.fixture
def mock_fernet_decrypt_invalid_token():
    with patch("odmantic_fernet_field.fernet_field.Fernet") as MockFernet:
        instance = MockFernet.return_value
        instance.decrypt.side_effect = InvalidToken
        yield MockFernet


@pytest.fixture
def mock_get_env_value():
    with patch("odmantic_fernet_field.fernet_field.get_env_value") as mock_env:
        mock_env.return_value = "testkey1,testkey2"
        yield mock_env


class TestBaseEncryptedString:
    def test_validate_bytes_success(self, mock_get_env_value, mock_fernet_decrypt_success):
        encrypted_bytes = b"encrypted"
        result = BaseEncryptedString.validate(encrypted_bytes)
        assert result == "decrypted_value"

    def test_validate_bytes_invalid_token(self, mock_get_env_value, mock_fernet_decrypt_invalid_token):
        encrypted_bytes = b"encrypted"
        result = BaseEncryptedString.validate(encrypted_bytes)
        assert result is None

    def test_validate_string(self):
        value = "plain string"
        result = BaseEncryptedString.validate(value)
        assert result == value

    def test_validate_invalid_type(self):
        with pytest.raises(TypeError):
            BaseEncryptedString.validate(123)


class TestBaseEncryptedInt:
    def test_validate_bytes_success(self, mock_get_env_value):
        with patch("odmantic_fernet_field.fernet_field.Fernet") as MockFernet:
            instance = MockFernet.return_value
            instance.decrypt.return_value = b"123"
            encrypted_bytes = b"encrypted"
            result = BaseEncryptedInt.validate(encrypted_bytes)
            assert result == 123

    def test_validate_bytes_invalid_token(self, mock_get_env_value, mock_fernet_decrypt_invalid_token):
        encrypted_bytes = b"encrypted"
        result = BaseEncryptedInt.validate(encrypted_bytes)
        assert result is None

    def test_validate_int(self):
        value = 456
        result = BaseEncryptedInt.validate(value)
        assert result == value

    def test_validate_invalid_type(self):
        with pytest.raises(TypeError):
            BaseEncryptedInt.validate("not an int")


class TestBaseEncryptedFloat:
    def test_validate_bytes_success(self, mock_get_env_value):
        with patch("odmantic_fernet_field.fernet_field.Fernet") as MockFernet:
            instance = MockFernet.return_value
            instance.decrypt.return_value = b"123.45"
            encrypted_bytes = b"encrypted"
            result = BaseEncryptedFloat.validate(encrypted_bytes)
            assert result == 123.45

    def test_validate_bytes_invalid_token(self, mock_get_env_value, mock_fernet_decrypt_invalid_token):
        encrypted_bytes = b"encrypted"
        result = BaseEncryptedFloat.validate(encrypted_bytes)
        assert result is None

    def test_validate_float(self):
        value = 789.01
        result = BaseEncryptedFloat.validate(value)
        assert result == value

    def test_validate_invalid_type(self):
        with pytest.raises(TypeError):
            BaseEncryptedFloat.validate("not a float")


class TestBaseEncryptedJSON:
    def test_validate_bytes_success(self, mock_get_env_value):
        sample_dict = {"key": "value", "date": datetime(2020, 1, 1)}
        json_str = json.dumps(sample_dict, default=str)
        with patch("odmantic_fernet_field.fernet_field.Fernet") as MockFernet:
            instance = MockFernet.return_value
            instance.decrypt.return_value = json.dumps({"key": "value", "date": "2020-01-01T00:00:00"}).encode()
            encrypted_bytes = b"encrypted"
            result = BaseEncryptedJSON.validate(encrypted_bytes)
            assert isinstance(result, dict)
            assert result["key"] == "value"
            assert isinstance(result["date"], datetime)

    def test_validate_bytes_invalid_token(self, mock_get_env_value, mock_fernet_decrypt_invalid_token):
        encrypted_bytes = b"encrypted"
        result = BaseEncryptedJSON.validate(encrypted_bytes)
        assert result is None

    def test_validate_dict(self):
        value = {"a": 1}
        result = BaseEncryptedJSON.validate(value)
        assert result == value

    def test_validate_invalid_type(self):
        with pytest.raises(TypeError):
            BaseEncryptedJSON.validate("not a dict")


class TestEncryptFunction:
    @patch("odmantic_fernet_field.fernet_field.get_env_value")
    @patch("odmantic_fernet_field.fernet_field.Fernet")
    def test_encrypt_string(self, MockFernet, mock_get_env_value):
        mock_get_env_value.return_value = "testkey"
        instance = MockFernet.return_value
        instance.encrypt.return_value = b"encrypted"
        result = encrypt("test string")
        assert result == b"encrypted"
        instance.encrypt.assert_called_once_with(b"test string")

    @patch("odmantic_fernet_field.fernet_field.get_env_value")
    @patch("odmantic_fernet_field.fernet_field.Fernet")
    def test_encrypt_int(self, MockFernet, mock_get_env_value):
        mock_get_env_value.return_value = "testkey"
        instance = MockFernet.return_value
        instance.encrypt.return_value = b"encrypted"
        result = encrypt(123)
        assert result == b"encrypted"
        instance.encrypt.assert_called_once_with(b"123")

    @patch("odmantic_fernet_field.fernet_field.get_env_value")
    @patch("odmantic_fernet_field.fernet_field.Fernet")
    def test_encrypt_float(self, MockFernet, mock_get_env_value):
        mock_get_env_value.return_value = "testkey"
        instance = MockFernet.return_value
        instance.encrypt.return_value = b"encrypted"
        result = encrypt(123.45)
        assert result == b"encrypted"
        instance.encrypt.assert_called_once_with(b"123.45")

    @patch("odmantic_fernet_field.fernet_field.get_env_value")
    @patch("odmantic_fernet_field.fernet_field.Fernet")
    def test_encrypt_dict(self, MockFernet, mock_get_env_value):
        mock_get_env_value.return_value = "testkey"
        instance = MockFernet.return_value
        instance.encrypt.return_value = b"encrypted"
        value = {"a": 1, "b": 2}
        result = encrypt(value)
        assert result == b"encrypted"
        # We cannot easily check the exact call argument because of CustomEncoder, so just check call count
        instance.encrypt.assert_called_once()

    def test_encrypt_invalid_type(self):
        with pytest.raises(TypeError):
            encrypt([1, 2, 3])
