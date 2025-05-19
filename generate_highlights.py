import os
import json
import logging
from urllib.parse import urlparse
from sentence_transformers import SentenceTransformer

from app.scraper.news_scraper import extract_article
from app.summarizer.summarizer import summarize
from app.deduplicator.deduplicator import cluster_articles
from app.highlights.highlight_maker import extract_highlights
from app.classifier.classifier import classify_article 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of URLs to scrape
urls = [
    # Technology
    "https://www.heraldsun.com.au/news/victoria/melbournes-new-cleaning-robots-will-use-ai-sophisticated-sensors-and-hitech-cameras/news-story/b53912b190bf9de64409d54a4aa92013",
    "https://www.news.com.au/technology/home-entertainment/tv/samsung-oled-s95-televisions-qseries-q990f-soundbar-hit-australian-market/news-story/491b5d2d657d2b7ab2a9d603d04debf4",
    "https://www.news.com.au/technology/innovation/littleknown-aussie-company-takes-on-china/news-story/ff6bf117ef94a0282d2cf0300c93c239",
    "https://www.news.com.au/technology/motoring/on-the-road/2025-paprika-53-model-25-gt-worlds-first-gravel-ebike-launches-in-australia/news-story/94a2cf1ae4b5ecad05b4b339e4bacc78",

    # Music
    "https://www.theguardian.com/tv-and-radio/2025/may/18/austrians-celebrate-jj-bringing-home-first-eurovision-win-in-11-years",
    "https://www.news.com.au/entertainment/music/australias-gojo-out-of-the-2025-eurovision-grand-final-in-a-stacked-semi/news-story/c323ed0ae37a6ff3687a04485b32bcf7",
    "https://www.nme.com/news/music/sam-fender-2025-australia-people-watching-tour-dates-tickets-3862851",

    # Finance
    "https://www.adelaidenow.com.au/real-estate/south-australia/adelaide/refinancing-surge-expected-across-sa-following-rba-decision/news-story/99b24a8c598fbc045abf52a401ab1927",
    "https://www.news.com.au/finance/business/dominos-australia-new-zealand-boss-announces-shock-resignation/news-story/d12258fa00bb9d34879255cf13789308",

    # Misc
    "https://www.news.com.au/national/nsw-act/news/woman-fighting-for-life-after-alleged-domestic-violence-assault/news-story/ff2ef4391acb67de34bea7dce26cbb6b",
    "https://www.abc.net.au/news/2025-05-18/lynas-rare-earths-breakthrough/13912346",
    "https://www.news.com.au/national/politics/abortion-a-matter-for-states-territories-liberal-senator-anne-ruston/news-story/28500d0e0f49ab0ebb6964249ed5eba7"
]

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def add_summary_to_articles(articles):
    for article in articles:
        try:
            text = article.get("text", "")
            if text:
                article["summary"] = summarize(text)
            else:
                article["summary"] = "No text to summarize."
        except Exception as e:
            logger.warning(f"Summarization failed for article {article.get('title')}: {e}")
            article["summary"] = text[:300] if text else "No summary available."


def add_source_to_articles(articles):
    for article in articles:
        try:
            parsed = urlparse(article["url"])
            article["source"] = parsed.netloc
        except Exception:
            article["source"] = "unknown"


def add_category_to_articles(articles):
    for article in articles:
        try:
            text = f"{article.get('title', '')}. {article.get('summary', '')}"
            article["category"] = classify_article(text)
        except Exception as e:
            logger.warning(f"Classification failed for article {article.get('title')}: {e}")
            article["category"] = "uncategorized"


def generate_embeddings(articles):
    texts = [article.get("text", "") for article in articles]
    return embedding_model.encode(texts)


def main():
    articles = []
    for url in urls:
        article = extract_article(url)
        if article:
            articles.append(article)

    if not articles:
        logger.error("No articles extracted. Exiting.")
        return

    add_summary_to_articles(articles)
    add_source_to_articles(articles)
    add_category_to_articles(articles) 

    embeddings = generate_embeddings(articles)

    cluster_articles(articles)

    highlights = extract_highlights(articles)

    categorized = {}
    for highlight in highlights:
        cat = highlight.get("category", "uncategorized")
        categorized.setdefault(cat, []).append(highlight)

    os.makedirs("data", exist_ok=True)
    with open("data/highlights.json", "w", encoding="utf-8") as f:
        json.dump(categorized, f, indent=2)

    logger.info("Highlights saved successfully to data/highlights.json")


if __name__ == "__main__":
    main()