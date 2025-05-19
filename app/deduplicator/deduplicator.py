def cluster_articles(articles):
    # Mock clustering: assign all articles to cluster 0
    for article in articles:
        article["cluster_id"] = 0
    return articles