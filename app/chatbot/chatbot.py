import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the highlights.json file
def load_highlights():
    with open('data/highlights.json', 'r') as f:
        return json.load(f)['uncategorized']

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to get the most relevant article based on the user's query
def get_answer(query):
    # Load the data (this can be done globally or inside the function)
    highlights = load_highlights()

    # Generate the query vector using the sentence-transformer model
    query_vec = model.encode(query).reshape(1, -1)
    
    # Generate embeddings for each article's text
    embeddings = []
    for article in highlights:
        try:
            article_vec = model.encode(article["text"]).reshape(1, -1)
            embeddings.append(article_vec)
        except KeyError:
            continue  # Skip articles that might be missing required data

    # Compute cosine similarity between the query and article embeddings
    scores = [cosine_similarity(query_vec, embedding)[0][0] for embedding in embeddings]
    
    # Get the index of the highest similarity score
    top_idx = np.argmax(scores)
    
    # Get the best-matching article
    best_article = highlights[top_idx]
    
    # Return the title and text of the best matching article
    return f"Title: {best_article.get('title', 'No Title Available')}\nSummary: {best_article.get('text', 'No Summary Available')}"