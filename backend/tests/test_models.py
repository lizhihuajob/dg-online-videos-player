import pytest
from app import models


class TestUserModel:
    def test_user_creation(self, db_session):
        user = models.User(
            username="modeltest",
            email="modeltest@example.com",
            hashed_password="hashedpassword123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "modeltest"
        assert user.email == "modeltest@example.com"
        assert user.created_at is not None

    def test_user_unique_username(self, db_session):
        user1 = models.User(
            username="uniqueuser",
            email="user1@example.com",
            hashed_password="hashedpassword"
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = models.User(
            username="uniqueuser",
            email="user2@example.com",
            hashed_password="hashedpassword"
        )
        db_session.add(user2)
        
        with pytest.raises(Exception):
            db_session.commit()


class TestPlayHistoryModel:
    def test_play_history_creation(self, db_session, test_user):
        history = models.PlayHistory(
            user_id=test_user.id,
            video_url="http://example.com/test.mp4",
            video_name="Test Video",
            video_format="mp4"
        )
        db_session.add(history)
        db_session.commit()
        db_session.refresh(history)
        
        assert history.id is not None
        assert history.user_id == test_user.id
        assert history.video_url == "http://example.com/test.mp4"
        assert history.created_at is not None


class TestLocalPlayHistoryModel:
    def test_local_play_history_creation(self, db_session, test_user):
        history = models.LocalPlayHistory(
            user_id=test_user.id,
            video_name="Local Test Video",
            video_format="webm",
            file_info='{"name": "test.webm", "size": 2048}'
        )
        db_session.add(history)
        db_session.commit()
        db_session.refresh(history)
        
        assert history.id is not None
        assert history.user_id == test_user.id
        assert history.video_name == "Local Test Video"
        assert history.video_format == "webm"
        assert history.file_info == '{"name": "test.webm", "size": 2048}'
