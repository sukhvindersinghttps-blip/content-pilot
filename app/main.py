import argparse, os
from dotenv import load_dotenv
from app.research.youtube_search import search_videos, fetch_video_and_channel_details
from app.analysis.outlier_detection import build_records
from app.agents.topic_agent import generate_opportunities
from app.agents.report_agent import write_report

def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Research recent YouTube outliers and generate content opportunities.")
    p.add_argument("--niche", required=True)
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--max-results", type=int, default=50)
    p.add_argument("--language", default="en")
    args = p.parse_args()
    if not os.getenv("YOUTUBE_API_KEY"):
        raise SystemExit("Missing YOUTUBE_API_KEY. Copy .env.example to .env and add your key.")
    items = search_videos(args.niche, args.days, args.max_results, args.language)
    video_ids = [x["id"]["videoId"] for x in items]
    channel_ids = [x["snippet"]["channelId"] for x in items]
    videos, channels = fetch_video_and_channel_details(video_ids, channel_ids)
    records = build_records(items, videos, channels)
    opportunities = generate_opportunities(args.niche, [r.to_dict() for r in records[:10]])
    md, js = write_report(args.niche, records, opportunities)
    print(f"Found {len(records)} videos.")
    print(f"Markdown report: {md}")
    print(f"JSON report: {js}")

if __name__ == "__main__": main()
