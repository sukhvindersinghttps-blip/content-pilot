from datetime import datetime
from pathlib import Path
import json

def write_report(niche, records, opportunities):
    Path("reports").mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md = Path("reports") / f"report_{stamp}.md"
    js = Path("reports") / f"report_{stamp}.json"
    lines = [f"# YouTube Content Opportunity Report: {niche}", "", f"Generated: {datetime.now().isoformat()}", "", "## Top Outliers", ""]
    for i, r in enumerate(records[:10], 1):
        lines += [f"### {i}. {r.title}", f"- Channel: {r.channel_title}", f"- Views: {r.views:,}", f"- Subscribers: {r.subscribers:,}", f"- Views/subscriber: {r.views_per_subscriber:.2f}", f"- Views/day: {r.views_per_day:,.0f}", f"- Outlier score: {r.outlier_score}", ""]
    lines += ["## Original Opportunities", ""]
    for i, o in enumerate(opportunities, 1):
        lines += [f"### {i}. {o.get('topic','Untitled')}", f"**Title:** {o.get('recommended_title','')}", f"**Angle:** {o.get('angle','')}", f"**Hook:** {o.get('hook','')}", f"**Thumbnail:** {o.get('thumbnail_concept','')}", f"**SEO:** {', '.join(o.get('seo_keywords', [])) if isinstance(o.get('seo_keywords', []), list) else o.get('seo_keywords','')}", f"**Why:** {o.get('rationale', o.get('reason',''))}", ""]
    md.write_text("\n".join(lines), encoding="utf-8")
    js.write_text(json.dumps({"niche": niche, "outliers": [r.to_dict() for r in records], "opportunities": opportunities}, ensure_ascii=False, indent=2), encoding="utf-8")
    return md, js
