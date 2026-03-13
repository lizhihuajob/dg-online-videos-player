import pytest


class TestPlayHistory:
    def test_add_play_history_success(self, client, auth_headers, sample_video_data):
        response = client.post("/history", json=sample_video_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["video_url"] == sample_video_data["video_url"]
        assert data["video_name"] == sample_video_data["video_name"]
        assert data["video_format"] == sample_video_data["video_format"]
        assert "id" in data
        assert "created_at" in data

    def test_add_play_history_duplicate_replaces_old(self, client, auth_headers, sample_video_data):
        # 添加第一条记录
        response = client.post("/history", json=sample_video_data, headers=auth_headers)
        assert response.status_code == 200
        first_id = response.json()["id"]

        # 添加相同视频的记录（应该替换旧的）
        response = client.post("/history", json=sample_video_data, headers=auth_headers)
        assert response.status_code == 200
        second_id = response.json()["id"]

        # 验证只有一条记录（旧记录被替换）
        response = client.get("/history", headers=auth_headers)
        assert len(response.json()) == 1
        # 新记录的ID可能与旧记录相同（取决于数据库实现）
        # 重点是记录被替换了，而不是ID是否不同

    def test_add_play_history_unauthorized(self, client, sample_video_data):
        response = client.post("/history", json=sample_video_data)
        assert response.status_code == 401

    def test_get_play_history_empty(self, client, auth_headers):
        response = client.get("/history", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_play_history_with_data(self, client, auth_headers, sample_video_data):
        # 添加播放历史
        client.post("/history", json=sample_video_data, headers=auth_headers)

        response = client.get("/history", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["video_url"] == sample_video_data["video_url"]
        assert data[0]["video_name"] == sample_video_data["video_name"]

    def test_get_play_history_order_and_limit(self, client, auth_headers):
        # 添加多条记录
        for i in range(15):
            video_data = {
                "video_url": f"https://example.com/video{i}.mp4",
                "video_name": f"视频{i}",
                "video_format": "mp4"
            }
            client.post("/history", json=video_data, headers=auth_headers)

        response = client.get("/history", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # 限制返回10条
        assert len(data) == 10
        # 按时间倒序排列
        for i in range(len(data) - 1):
            assert data[i]["created_at"] >= data[i + 1]["created_at"]

    def test_get_play_history_unauthorized(self, client):
        response = client.get("/history")
        assert response.status_code == 401

    def test_delete_play_history_success(self, client, auth_headers, sample_video_data):
        # 添加记录
        response = client.post("/history", json=sample_video_data, headers=auth_headers)
        history_id = response.json()["id"]

        # 删除记录
        response = client.delete(f"/history/{history_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # 确认已删除
        response = client.get("/history", headers=auth_headers)
        assert len(response.json()) == 0

    def test_delete_play_history_not_found(self, client, auth_headers):
        response = client.delete("/history/999", headers=auth_headers)
        assert response.status_code == 404
        assert "History item not found" in response.json()["detail"]

    def test_delete_play_history_other_user(self, client, auth_headers, sample_video_data, test_user2):
        # 创建第二个用户
        client.post("/register", json=test_user2)
        response = client.post(
            "/token",
            data={
                "username": test_user2["username"],
                "password": test_user2["password"]
            }
        )
        token2 = response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        # 第一个用户添加记录
        response = client.post("/history", json=sample_video_data, headers=auth_headers)
        history_id = response.json()["id"]

        # 第二个用户尝试删除
        response = client.delete(f"/history/{history_id}", headers=headers2)
        assert response.status_code == 404

    def test_clear_play_history_success(self, client, auth_headers, sample_video_data):
        # 添加多条记录
        for i in range(3):
            video_data = {
                "video_url": f"https://example.com/video{i}.mp4",
                "video_name": f"视频{i}",
                "video_format": "mp4"
            }
            client.post("/history", json=video_data, headers=auth_headers)

        # 清空历史
        response = client.delete("/history", headers=auth_headers)
        assert response.status_code == 200
        assert "All history cleared successfully" in response.json()["message"]

        # 确认已清空
        response = client.get("/history", headers=auth_headers)
        assert len(response.json()) == 0

    def test_clear_play_history_only_affects_current_user(self, client, auth_headers, sample_video_data, test_user2):
        # 添加记录到第一个用户
        client.post("/history", json=sample_video_data, headers=auth_headers)

        # 创建第二个用户并添加记录
        client.post("/register", json=test_user2)
        response = client.post(
            "/token",
            data={
                "username": test_user2["username"],
                "password": test_user2["password"]
            }
        )
        token2 = response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        video_data2 = {
            "video_url": "https://example.com/other.mp4",
            "video_name": "其他视频",
            "video_format": "mp4"
        }
        client.post("/history", json=video_data2, headers=headers2)

        # 第一个用户清空历史
        client.delete("/history", headers=auth_headers)

        # 第二个用户的历史应该还在
        response = client.get("/history", headers=headers2)
        assert len(response.json()) == 1
