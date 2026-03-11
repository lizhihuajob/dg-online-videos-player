from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PlaybackRecord:
    id: Optional[int]
    video_url: str
    video_name: str
    video_format: str
    last_position: float
    play_count: int
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            'id': self.id,
            'video_url': self.video_url,
            'video_name': self.video_name,
            'video_format': self.video_format,
            'last_position': self.last_position,
            'play_count': self.play_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data: dict):
        return PlaybackRecord(
            id=data.get('id'),
            video_url=data.get('video_url', ''),
            video_name=data.get('video_name', ''),
            video_format=data.get('video_format', 'mp4'),
            last_position=data.get('last_position', 0),
            play_count=data.get('play_count', 1),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
