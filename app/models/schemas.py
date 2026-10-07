from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class VideoRecord:
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    published_at: str
    views: int
    likes: int
    comments: int
    subscribers: int
    duration_seconds: int
    description: str = ""
    outlier_score: float = 0.0
    views_per_day: float = 0.0
    views_per_subscriber: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
