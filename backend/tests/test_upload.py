import pytest
from io import BytesIO


class TestUpload:
    def test_upload_video_success(self, client, auth_headers):
        # 创建模拟视频文件
        video_content = b"fake video content"
        response = client.post(
            "/upload",
            files={"file": ("test.mp4", BytesIO(video_content), "video/mp4")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.mp4"
        assert "url" in data
        assert data["format"] == "mp4"
        assert data["url"].startswith("/uploads/")

    def test_upload_video_webm(self, client, auth_headers):
        video_content = b"fake webm content"
        response = client.post(
            "/upload",
            files={"file": ("test.webm", BytesIO(video_content), "video/webm")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.webm"
        assert data["format"] == "webm"

    def test_upload_video_unauthorized(self, client):
        video_content = b"fake video content"
        response = client.post(
            "/upload",
            files={"file": ("test.mp4", BytesIO(video_content), "video/mp4")}
        )
        assert response.status_code == 401

    def test_upload_non_video_file(self, client, auth_headers):
        # 尝试上传非视频文件
        text_content = b"this is a text file"
        response = client.post(
            "/upload",
            files={"file": ("test.txt", BytesIO(text_content), "text/plain")},
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "File must be a video" in response.json()["detail"]

    def test_upload_video_no_extension(self, client, auth_headers):
        # 上传没有扩展名的文件
        video_content = b"fake video content"
        response = client.post(
            "/upload",
            files={"file": ("testvideo", BytesIO(video_content), "video/mp4")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # 没有扩展名时，format 为空字符串
        assert data["format"] == ""  # 实际行为：没有扩展名返回空字符串

    def test_upload_video_large_filename(self, client, auth_headers):
        # 上传文件名很长的视频
        video_content = b"fake video content"
        long_filename = "a" * 200 + ".mp4"
        response = client.post(
            "/upload",
            files={"file": (long_filename, BytesIO(video_content), "video/mp4")},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == long_filename
