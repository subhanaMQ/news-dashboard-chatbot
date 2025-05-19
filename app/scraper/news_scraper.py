import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def detect_category_keyword(text):
    text_lower = text.lower()
    categories_keywords = {
        "sports": ["football", "soccer", "basketball", "tennis", "game", "player"],
        "lifestyle": ["fashion", "travel", "food", "culture", "lifestyle", "wellness"],
        "music": ["music", "album", "song", "concert", "band", "singer"],
        "finance": ["market", "stocks", "finance", "economy", "investment", "money"],
        "politics": ["election", "government", "president", "politics", "senate"],
        "technology": ["technology", "software", "hardware", "ai", "computer", "gadgets"],
        "health": ["health", "medicine", "doctor", "disease", "wellness", "covid"],
        "world": ["international", "world", "global", "united nations", "foreign"],
        "national": ["national", "local", "state", "government"]
    }

    for category, keywords in categories_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return "uncategorized"

def extract_article(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "No title"

        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text() for p in paragraphs)

        if len(text.strip()) < 100:
            raise Exception("Article content too short or not found.")

        category = detect_category_keyword(text)

        # Extract source domain
        parsed_url = urlparse(url)
        source = parsed_url.netloc

        # Attempt to extract author (generic approach)
        author = "unknown"
        author_tag = soup.find('meta', attrs={"name": "author"})
        if author_tag and author_tag.get("content"):
            author = author_tag["content"]
        else:
            author_tag = soup.find('meta', attrs={"property": "article:author"})
            if author_tag and author_tag.get("content"):
                author = author_tag["content"]

        logger.info(f"Successfully extracted article from {url} with category '{category}'")
        return {
            "url": url,
            "title": title,
            "text": text,
            "category": category,
            "source": source,
            "author": author,
            "frequency": 1  # Default frequency, to be updated later
        }

    except Exception as e:
        logger.error(f"Failed to extract article from {url}: {e}")
        return None