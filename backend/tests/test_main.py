import pytest
import os
import tempfile
from io import BytesIO


def test_root_endpoint(client):
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Video Player API is running"}


class TestUserAuthentication:
    """用户认证相关测试"""

    def test_register_new_user(self, client, db):
        """测试新用户注册"""
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
        """测试重复用户名注册失败"""
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
        """测试重复邮箱注册失败"""
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

    def test_register_invalid_email_format(self, client, db):
        """测试无效邮箱格式 - 当前 API 接受任意格式邮箱"""
        # 注：当前 API 未对邮箱格式做严格验证，此测试验证 API 行为
        response = client.post(
            "/register",
            json={"username": "invalidemail", "email": "not-an-email", "password": "pass123"}
        )
        # 当前实现接受任意邮箱格式，返回 200
        assert response.status_code == 200

    def test_register_short_password(self, client, db):
        """测试短密码注册"""
        response = client.post(
            "/register",
            json={"username": "shortpass", "email": "short@example.com", "password": "123"}
        )
        assert response.status_code == 200

    def test_login_success(self, client, db):
        """测试登录成功"""
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
        """测试错误密码登录失败"""
        client.post(
            "/register",
            json={"username": "wrongpass", "email": "wrong@example.com", "password": "correct123"}
        )
        response = client.post(
            "/token",
            data={"username": "wrongpass", "password": "wrong123"}
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client, db):
        """测试不存在的用户登录失败"""
        response = client.post(
            "/token",
            data={"username": "nonexistent", "password": "anypass123"}
        )
        assert response.status_code == 401

    def test_get_current_user(self, client, auth_headers):
        """测试获取当前用户信息"""
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    def test_get_current_user_unauthorized(self, client):
        """测试未授权获取用户信息失败"""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        """测试无效 token 获取用户信息失败"""
        response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401


class TestUserProfileUpdate:
    """用户信息更新测试"""

    def test_update_user_info(self, client, auth_headers, db):
        """测试更新用户信息"""
        response = client.put(
            "/users/me",
            json={"username": "updateduser", "email": "updated@example.com"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["email"] == "updated@example.com"

    def test_update_user_duplicate_username(self, client, auth_headers, db):
        """测试更新为已存在的用户名失败"""
        client.post(
            "/register",
            json={"username": "existinguser", "email": "existing@example.com", "password": "pass123"}
        )
        response = client.put(
            "/users/me",
            json={"username": "existinguser", "email": "newemail@example.com"},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_update_user_duplicate_email(self, client, auth_headers, db):
        """测试更新为已存在的邮箱失败"""
        client.post(
            "/register",
            json={"username": "existinguser2", "email": "existing2@example.com", "password": "pass123"}
        )
        response = client.put(
            "/users/me",
            json={"username": "testuser", "email": "existing2@example.com"},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_update_user_unauthorized(self, client):
        """测试未授权更新用户信息失败"""
        response = client.put(
            "/users/me",
            json={"username": "newname", "email": "new@example.com"}
        )
        assert response.status_code == 401


class TestPasswordUpdate:
    """密码修改测试"""

    def test_update_password_success(self, client, auth_headers, db):
        """测试成功修改密码"""
        response = client.put(
            "/users/me/password",
            json={"current_password": "testpass123", "new_password": "newpass456"},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Password updated successfully" in response.json()["message"]

        # 验证新密码可以登录
        login_response = client.post(
            "/token",
            data={"username": "testuser", "password": "newpass456"}
        )
        assert login_response.status_code == 200

    def test_update_password_wrong_current(self, client, auth_headers, db):
        """测试错误当前密码修改失败"""
        response = client.put(
            "/users/me/password",
            json={"current_password": "wrongpass", "new_password": "newpass456"},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Current password is incorrect" in response.json()["detail"]

    def test_update_password_unauthorized(self, client):
        """测试未授权修改密码失败"""
        response = client.put(
            "/users/me/password",
            json={"current_password": "anypass", "new_password": "newpass456"}
        )
        assert response.status_code == 401


class TestPlayHistory:
    """播放历史测试"""

    def test_add_play_history(self, client, auth_headers):
        """测试添加播放历史"""
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
        """测试重复添加播放历史（应更新而不是创建新记录）"""
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
        """测试获取播放历史"""
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

    def test_get_play_history_unauthorized(self, client):
        """测试未授权获取播放历史失败"""
        response = client.get("/history")
        assert response.status_code == 401

    def test_delete_play_history(self, client, auth_headers):
        """测试删除播放历史"""
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
        """测试删除不存在的播放历史"""
        response = client.delete("/history/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_play_history_unauthorized(self, client):
        """测试未授权删除播放历史失败"""
        response = client.delete("/history/1")
        assert response.status_code == 401

    def test_clear_play_history(self, client, auth_headers):
        """测试清空播放历史"""
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
    """本地播放历史测试"""

    def test_add_local_play_history(self, client, auth_headers):
        """测试添加本地播放历史"""
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
        """测试获取本地播放历史"""
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

    def test_get_local_play_history_unauthorized(self, client):
        """测试未授权获取本地播放历史失败"""
        response = client.get("/local-history")
        assert response.status_code == 401

    def test_delete_local_play_history(self, client, auth_headers):
        """测试删除本地播放历史"""
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

    def test_delete_local_play_history_not_found(self, client, auth_headers):
        """测试删除不存在的本地播放历史"""
        response = client.delete("/local-history/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_clear_local_play_history(self, client, auth_headers):
        """测试清空本地播放历史"""
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
    """视频上传测试"""

    def test_upload_video_unauthorized(self, client):
        """测试未授权上传视频失败"""
        file_content = BytesIO(b"fake video content")
        response = client.post(
            "/upload",
            files={"file": ("test.mp4", file_content, "video/mp4")}
        )
        assert response.status_code == 401

    def test_upload_non_video_file(self, client, auth_headers):
        """测试上传非视频文件失败"""
        file_content = BytesIO(b"not a video")
        response = client.post(
            "/upload",
            files={"file": ("test.txt", file_content, "text/plain")},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "File must be a video" in response.json()["detail"]

    def test_upload_image_file(self, client, auth_headers):
        """测试上传图片文件失败"""
        file_content = BytesIO(b"fake image content")
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", file_content, "image/jpeg")},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "File must be a video" in response.json()["detail"]

    def test_upload_video_success(self, client, auth_headers):
        """测试成功上传视频文件"""
        file_content = BytesIO(b"fake video content for testing")
        response = client.post(
            "/upload",
            files={"file": ("test_video.mp4", file_content, "video/mp4")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "filename" in data
        assert "url" in data
        assert "format" in data
        assert data["filename"] == "test_video.mp4"
        assert data["format"] == "mp4"
        assert "/uploads/" in data["url"]

    def test_upload_different_video_formats(self, client, auth_headers):
        """测试上传不同格式的视频文件"""
        formats = [
            ("test.webm", "video/webm"),
            ("test.ogv", "video/ogg"),
            ("test.mov", "video/quicktime"),
        ]
        for filename, content_type in formats:
            file_content = BytesIO(b"fake video content")
            response = client.post(
                "/upload",
                files={"file": (filename, file_content, content_type)},
                headers=auth_headers
            )
            assert response.status_code == 200, f"Failed for {filename}"
            assert response.json()["format"] == filename.split(".")[-1]
