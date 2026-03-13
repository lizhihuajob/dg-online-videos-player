import pytest
from app import auth


class TestPasswordHashing:
    def test_verify_password_correct(self):
        password = "testpassword123"
        hashed = auth.get_password_hash(password)
        assert auth.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = auth.get_password_hash(password)
        assert auth.verify_password(wrong_password, hashed) is False

    def test_get_password_hash_generates_different_hashes(self):
        password = "testpassword123"
        hash1 = auth.get_password_hash(password)
        hash2 = auth.get_password_hash(password)
        # 相同的密码应该生成不同的哈希值（因为使用了随机盐）
        assert hash1 != hash2
        # 但两者都应该能验证通过
        assert auth.verify_password(password, hash1) is True
        assert auth.verify_password(password, hash2) is True


class TestJWTToken:
    def test_create_access_token(self):
        data = {"sub": "1"}
        token = auth.create_access_token(data)
        assert token is not None
        assert isinstance(token, str)

    def test_create_access_token_with_expiry(self):
        from datetime import timedelta
        data = {"sub": "1"}
        expires = timedelta(minutes=30)
        token = auth.create_access_token(data, expires_delta=expires)
        assert token is not None


class TestAuthIntegration:
    def test_register_success(self, client, test_user):
        response = client.post("/register", json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user["username"]
        assert data["email"] == test_user["email"]
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user):
        # 先注册一个用户
        response = client.post("/register", json=test_user)
        assert response.status_code == 200

        # 再次使用相同用户名注册
        duplicate_user = {
            "username": test_user["username"],
            "email": "different@example.com",
            "password": "password123"
        }
        response = client.post("/register", json=duplicate_user)
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user):
        # 先注册一个用户
        response = client.post("/register", json=test_user)
        assert response.status_code == 200

        # 再次使用相同邮箱注册
        duplicate_user = {
            "username": "differentuser",
            "email": test_user["email"],
            "password": "password123"
        }
        response = client.post("/register", json=duplicate_user)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_login_success(self, client, registered_user):
        response = client.post(
            "/token",
            data={
                "username": registered_user["username"],
                "password": registered_user["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == registered_user["username"]

    def test_login_wrong_password(self, client, registered_user):
        response = client.post(
            "/token",
            data={
                "username": registered_user["username"],
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/token",
            data={
                "username": "nonexistentuser",
                "password": "password123"
            }
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_get_current_user_success(self, client, auth_headers, registered_user):
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == registered_user["username"]
        assert data["email"] == registered_user["email"]

    def test_get_current_user_no_token(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalidtoken"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401
