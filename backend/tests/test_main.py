import pytest
from io import BytesIO


class TestRootEndpoint:
    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Video Player API is running"}


class TestUserRegistration:
    def test_register_success(self, client):
        response = client.post(
            "/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user):
        response = client.post(
            "/register",
            json={
                "username": "testuser",
                "email": "another@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user):
        response = client.post(
            "/register",
            json={
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]


class TestUserLogin:
    def test_login_success(self, client, test_user):
        response = client.post(
            "/token",
            data={"username": "testuser", "password": "testpassword123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"

    def test_login_wrong_password(self, client, test_user):
        response = client.post(
            "/token",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/token",
            data={"username": "nonexistent", "password": "password123"}
        )
        assert response.status_code == 401


class TestUserMe:
    def test_get_current_user_success(self, client, auth_headers):
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_current_user_no_token(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        response = client.get("/users/me", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401


class TestPlayHistory:
    def test_add_play_history(self, client, auth_headers):
        response = client.post(
            "/history",
            json={
                "video_url": "http://example.com/video.mp4",
                "video_name": "Test Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_url"] == "http://example.com/video.mp4"
        assert data["video_name"] == "Test Video"

    def test_get_play_history(self, client, auth_headers):
        client.post(
            "/history",
            json={
                "video_url": "http://example.com/video.mp4",
                "video_name": "Test Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        response = client.get("/history", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["video_name"] == "Test Video"

    def test_delete_play_history(self, client, auth_headers):
        add_response = client.post(
            "/history",
            json={
                "video_url": "http://example.com/video.mp4",
                "video_name": "Test Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        history_id = add_response.json()["id"]
        
        response = client.delete(f"/history/{history_id}", headers=auth_headers)
        assert response.status_code == 200

    def test_clear_play_history(self, client, auth_headers):
        client.post(
            "/history",
            json={
                "video_url": "http://example.com/video.mp4",
                "video_name": "Test Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        response = client.delete("/history", headers=auth_headers)
        assert response.status_code == 200

    def test_play_history_unauthorized(self, client):
        response = client.get("/history")
        assert response.status_code == 401


class TestLocalPlayHistory:
    def test_add_local_play_history(self, client, auth_headers):
        response = client.post(
            "/local-history",
            json={
                "video_name": "Local Video",
                "video_format": "mp4",
                "file_info": '{"name": "video.mp4", "size": 1024}'
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_name"] == "Local Video"

    def test_get_local_play_history(self, client, auth_headers):
        client.post(
            "/local-history",
            json={
                "video_name": "Local Video",
                "video_format": "mp4",
                "file_info": '{"name": "video.mp4", "size": 1024}'
            },
            headers=auth_headers
        )
        response = client.get("/local-history", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_delete_local_play_history(self, client, auth_headers):
        add_response = client.post(
            "/local-history",
            json={
                "video_name": "Local Video",
                "video_format": "mp4",
                "file_info": '{"name": "video.mp4", "size": 1024}'
            },
            headers=auth_headers
        )
        history_id = add_response.json()["id"]
        
        response = client.delete(f"/local-history/{history_id}", headers=auth_headers)
        assert response.status_code == 200

    def test_clear_local_play_history(self, client, auth_headers):
        client.post(
            "/local-history",
            json={
                "video_name": "Local Video",
                "video_format": "mp4",
                "file_info": '{"name": "video.mp4", "size": 1024}'
            },
            headers=auth_headers
        )
        response = client.delete("/local-history", headers=auth_headers)
        assert response.status_code == 200


class TestVideoUpload:
    def test_upload_video_unauthorized(self, client):
        video_content = b"fake video content"
        response = client.post(
            "/upload",
            files={"file": ("test.mp4", BytesIO(video_content), "video/mp4")}
        )
        assert response.status_code == 401

    def test_upload_non_video_file(self, client, auth_headers):
        text_content = b"not a video"
        response = client.post(
            "/upload",
            files={"file": ("test.txt", BytesIO(text_content), "text/plain")},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "File must be a video" in response.json()["detail"]
