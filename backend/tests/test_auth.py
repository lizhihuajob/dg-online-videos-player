import pytest
from datetime import timedelta
from app.auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt

class TestPasswordHashing:
    def test_password_hash_and_verify(self):
        password = "mysecretpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        password = "correctpassword"
        wrong = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong, hashed) is False

    def test_hash_is_unique(self):
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2


class TestTokenCreation:
    def test_create_access_token(self):
        data = {"sub": "123"}
        token = create_access_token(data)
        assert token is not None
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "123"
        assert "exp" in decoded

    def test_create_access_token_with_expiration(self):
        data = {"sub": "456"}
        expires = timedelta(minutes=15)
        token = create_access_token(data, expires_delta=expires)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "456"
