import pytest
import os
import tempfile
from io import BytesIO

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Video Player API is running"}


class TestUserAuthentication:
    def test_register_new_user(self, client, db):
        response = client.post(
            "/register",
            json={"username": "newuser", "email": "new@example.com", "password": "newpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "password" not in data

    def test_register_duplicate_username(self, client, db):
        client.post(
            "/register",
            json={"username": "dupuser", "email": "dup1@example.com", "password": "pass123"}
        )
        response = client.post(
            "/register",
            json={"username": "dupuser", "email": "dup2@example.com", "password": "pass123"}
        )
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, db):
        client.post(
            "/register",
            json={"username": "user1", "email": "dup@example.com", "password": "pass123"}
        )
        response = client.post(
            "/register",
            json={"username": "user2", "email": "dup@example.com", "password": "pass123"}
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_login_success(self, client, db):
        client.post(
            "/register",
            json={"username": "loginuser", "email": "login@example.com", "password": "mypass123"}
        )
        response = client.post(
            "/token",
            data={"username": "loginuser", "password": "mypass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "loginuser"

    def test_login_wrong_password(self, client, db):
        client.post(
            "/register",
            json={"username": "wrongpass", "email": "wrong@example.com", "password": "correct123"}
        )
        response = client.post(
            "/token",
            data={"username": "wrongpass", "password": "wrong123"}
        )
        assert response.status_code == 401

    def test_get_current_user(self, client, auth_headers):
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    def test_get_current_user_unauthorized(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401


class TestPlayHistory:
    def test_add_play_history(self, client, auth_headers):
        response = client.post(
            "/history",
            json={
                "video_url": "http://example.com/test.mp4",
                "video_name": "Test Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_url"] == "http://example.com/test.mp4"
        assert data["video_name"] == "Test Video"
        assert "id" in data
        assert "created_at" in data

    def test_add_duplicate_play_history(self, client, auth_headers):
        client.post(
            "/history",
            json={
                "video_url": "http://example.com/dup.mp4",
                "video_name": "Dup Video",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        response = client.post(
            "/history",
            json={
                "video_url": "http://example.com/dup.mp4",
                "video_name": "Dup Video 2",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        history = client.get("/history", headers=auth_headers)
        assert len(history.json()) == 1

    def test_get_play_history(self, client, auth_headers):
        client.post(
            "/history",
            json={
                "video_url": "http://example.com/v1.mp4",
                "video_name": "Video 1",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        response = client.get("/history", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_delete_play_history(self, client, auth_headers):
        add_response = client.post(
            "/history",
            json={
                "video_url": "http://example.com/del.mp4",
                "video_name": "Delete Me",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        history_id = add_response.json()["id"]
        response = client.delete(f"/history/{history_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

    def test_delete_play_history_not_found(self, client, auth_headers):
        response = client.delete("/history/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_clear_play_history(self, client, auth_headers):
        client.post(
            "/history",
            json={
                "video_url": "http://example.com/clear1.mp4",
                "video_name": "Clear 1",
                "video_format": "mp4"
            },
            headers=auth_headers
        )
        response = client.delete("/history", headers=auth_headers)
        assert response.status_code == 200
        history = client.get("/history", headers=auth_headers)
        assert len(history.json()) == 0


class TestLocalPlayHistory:
    def test_add_local_play_history(self, client, auth_headers):
        response = client.post(
            "/local-history",
            json={
                "video_name": "Local Video",
                "video_format": "mp4",
                "file_info": '{"name": "test.mp4", "size": 1024}'
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["video_name"] == "Local Video"
        assert "file_info" in data

    def test_get_local_play_history(self, client, auth_headers):
        client.post(
            "/local-history",
            json={
                "video_name": "Local Test",
                "video_format": "webm",
                "file_info": "{}"
            },
            headers=auth_headers
        )
        response = client.get("/local-history", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_delete_local_play_history(self, client, auth_headers):
        add_response = client.post(
            "/local-history",
            json={
                "video_name": "Delete Local",
                "video_format": "mp4",
                "file_info": "{}"
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
                "video_name": "Clear Local",
                "video_format": "mp4",
                "file_info": "{}"
            },
            headers=auth_headers
        )
        response = client.delete("/local-history", headers=auth_headers)
        assert response.status_code == 200
        history = client.get("/local-history", headers=auth_headers)
        assert len(history.json()) == 0


class TestVideoUpload:
    def test_upload_video_unauthorized(self, client):
        file_content = BytesIO(b"fake video content")
        response = client.post(
            "/upload",
            files={"file": ("test.mp4", file_content, "video/mp4")}
        )
        assert response.status_code == 401

    def test_upload_non_video_file(self, client, auth_headers):
        file_content = BytesIO(b"not a video")
        response = client.post(
            "/upload",
            files={"file": ("test.txt", file_content, "text/plain")},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "File must be a video" in response.json()["detail"]
