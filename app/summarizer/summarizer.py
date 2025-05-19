def summarize(text):
    # Simple mock summarization: first 3 sentences or 300 chars max
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = ' '.join(sentences[:3])
    if len(summary) > 300:
        summary = summary[:300] + "..."
    return summary