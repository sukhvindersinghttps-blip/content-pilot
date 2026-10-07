import json, os
from openai import OpenAI

def generate_opportunities(niche: str, outliers: list[dict], count: int = 8):
    if not os.getenv("OPENAI_API_KEY"):
        return [{"topic": f"Original {niche} topic inspired by the strongest recent pattern", "reason": "Configure OPENAI_API_KEY for AI-generated opportunities."} for _ in range(count)]
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f'''You are a YouTube content strategist. Niche: {niche}.
Analyze these recent outlier videos and extract patterns, then propose {count} ORIGINAL video opportunities.
Do not copy titles, scripts, thumbnails, or distinctive wording. Reuse only high-level audience-demand patterns.
Return JSON array with fields: topic, recommended_title, alternative_titles, angle, hook, thumbnail_concept, seo_keywords, rationale, opportunity_score.
Outliers:\n{json.dumps(outliers, ensure_ascii=False)}'''
    response = client.chat.completions.create(model=os.getenv("OPENAI_MODEL", "gpt-5.6"), messages=[{"role":"user","content":prompt}], temperature=0.8)
    text = response.choices[0].message.content or "[]"
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return [{"topic": "Parsing error", "raw": text}]
