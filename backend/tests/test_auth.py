import pytest
from datetime import timedelta
from app.auth import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt


class TestPasswordHashing:
    """密码哈希相关测试"""

    def test_password_hash_and_verify(self):
        """测试密码哈希和验证"""
        password = "mysecretpassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        """测试错误密码验证失败"""
        password = "correctpassword"
        wrong = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong, hashed) is False

    def test_hash_is_unique(self):
        """测试相同密码生成不同哈希值（盐值随机）"""
        password = "samepassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_verify_password_with_empty_string(self):
        """测试空密码验证"""
        password = ""
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
        assert verify_password("notempty", hashed) is False


class TestTokenCreation:
    """JWT Token 相关测试"""

    def test_create_access_token(self):
        """测试创建访问令牌"""
        data = {"sub": "123"}
        token = create_access_token(data)
        assert token is not None
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "123"
        assert "exp" in decoded

    def test_create_access_token_with_expiration(self):
        """测试创建带过期时间的令牌"""
        data = {"sub": "456"}
        expires = timedelta(minutes=15)
        token = create_access_token(data, expires_delta=expires)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "456"

    def test_create_access_token_with_additional_data(self):
        """测试创建包含额外数据的令牌"""
        data = {"sub": "789", "username": "testuser", "role": "admin"}
        token = create_access_token(data)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "789"
        assert decoded["username"] == "testuser"
        assert decoded["role"] == "admin"
