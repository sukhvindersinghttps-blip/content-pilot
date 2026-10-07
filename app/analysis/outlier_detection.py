from datetime import datetime, timezone
import re
from app.models.schemas import VideoRecord

def iso_duration_to_seconds(value: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not m: return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s

def build_records(items, videos, channels):
    records = []
    now = datetime.now(timezone.utc)
    for item in items:
        vid = item["id"]["videoId"]
        v = videos.get(vid)
        if not v: continue
        stats = v.get("statistics", {})
        sn = v.get("snippet", {})
        ch = channels.get(sn.get("channelId"), {}).get("statistics", {})
        published = datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        age_days = max((now - published).total_seconds() / 86400, 0.25)
        views = int(stats.get("viewCount", 0))
        subs = max(int(ch.get("subscriberCount", 0)), 1)
        rec = VideoRecord(
            video_id=vid, title=sn.get("title", ""), channel_id=sn.get("channelId", ""),
            channel_title=sn.get("channelTitle", ""), published_at=sn.get("publishedAt", ""),
            views=views, likes=int(stats.get("likeCount", 0)), comments=int(stats.get("commentCount", 0)),
            subscribers=subs, duration_seconds=iso_duration_to_seconds(v.get("contentDetails", {}).get("duration", "")),
            description=sn.get("description", ""), views_per_day=views/age_days,
            views_per_subscriber=views/subs,
        )
        # Log-scaled, transparent heuristic. No claim of guaranteed virality.
        import math
        rec.outlier_score = round((math.log10(rec.views_per_subscriber + 1) * 60) + (math.log10(rec.views_per_day + 1) * 10), 2)
        records.append(rec)
    return sorted(records, key=lambda x: x.outlier_score, reverse=True)
