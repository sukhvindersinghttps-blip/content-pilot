import os
from datetime import datetime, timedelta, timezone
import requests

BASE = "https://www.googleapis.com/youtube/v3"

def _get(path, params):
    r = requests.get(f"{BASE}/{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def search_videos(query: str, days: int = 7, max_results: int = 50, language: str = "en"):
    key = os.environ["YOUTUBE_API_KEY"]
    published_after = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat().replace("+00:00", "Z")
    data = _get("search", {
        "part": "snippet", "q": query, "type": "video", "order": "viewCount",
        "publishedAfter": published_after, "maxResults": min(max_results, 50),
        "relevanceLanguage": language, "key": key,
    })
    return data.get("items", [])

def fetch_video_and_channel_details(video_ids: list[str], channel_ids: list[str]):
    key = os.environ["YOUTUBE_API_KEY"]
    videos, channels = {}, {}
    for i in range(0, len(video_ids), 50):
        data = _get("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(video_ids[i:i+50]), "key": key})
        for item in data.get("items", []): videos[item["id"]] = item
    for i in range(0, len(channel_ids), 50):
        data = _get("channels", {"part": "statistics", "id": ",".join(channel_ids[i:i+50]), "key": key})
        for item in data.get("items", []): channels[item["id"]] = item
    return videos, channels
