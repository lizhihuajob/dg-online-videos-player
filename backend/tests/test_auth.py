import pytest
from app import auth


class TestPasswordHashing:
    def test_get_password_hash(self):
        password = "testpassword123"
        hashed = auth.get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        password = "testpassword123"
        hashed = auth.get_password_hash(password)
        assert auth.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = auth.get_password_hash(password)
        assert auth.verify_password(wrong_password, hashed) is False

    def test_different_passwords_different_hashes(self):
        password = "testpassword123"
        hash1 = auth.get_password_hash(password)
        hash2 = auth.get_password_hash(password)
        assert hash1 != hash2


class TestAccessToken:
    def test_create_access_token(self):
        data = {"sub": "1"}
        token = auth.create_access_token(data)
        assert token is not None
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        from datetime import timedelta
        data = {"sub": "1"}
        token = auth.create_access_token(data, expires_delta=timedelta(minutes=30))
        assert token is not None

    def test_access_token_contains_data(self):
        from jose import jwt
        data = {"sub": "123"}
        token = auth.create_access_token(data)
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        assert payload["sub"] == "123"
