def extract_highlights(articles):
    # Mock highlight extraction: return article summaries as highlights
    highlights = []
    for art in articles:
        highlights.append({
            "title": art.get("title", ""),
            "summary": art.get("summary", ""),
            "category": art.get("category", "uncategorized"),
            "source": art.get("source", "unknown"),
            "url": art.get("url", "")
        })
    return highlights