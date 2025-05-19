import streamlit as st
import json
import numpy as np
import re
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# MUST be the first Streamlit command
st.set_page_config(page_title="News Dashboard + Chatbot", layout="wide")

# ====== GroqCloud Setup ======
GROQ_API_KEY = "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" 
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

def ask_groq(query, context):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions about news articles."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    data = {
        "model": GROQ_MODEL,
        "messages": messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ====== Load Data ======
@st.cache_data
def load_highlights():
    with open("data/highlights.json") as f:
        return json.load(f)

# ====== Load Embedding Model ======
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_model()

# ====== Helpers ======
def split_into_sentences(text):
    # Simple sentence splitter by punctuation + space
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

def get_top_k_articles(query, articles, k=3):
    filtered_articles = [
        a for a in articles if a.get("text") or a.get("summary") or a.get("title")
    ]
    query_vec = embedding_model.encode(query).reshape(1, -1)
    article_vecs = [
        embedding_model.encode(
            a.get("text") or a.get("summary") or a.get("title")
        )
        for a in filtered_articles
    ]
    similarities = cosine_similarity(query_vec, article_vecs)[0]
    top_indices = np.argsort(similarities)[-k:][::-1]
    return [filtered_articles[i] for i in top_indices]

# ====== UI ======
st.title("📰 News Highlights + Chatbot")

highlights = load_highlights()
categories = list(highlights.keys())

# Optional: add an "All" option at the start
categories = ["All"] + categories
selected = st.selectbox("Choose category", categories)

if selected == "All":
    # Combine all articles from all categories
    filtered_highlights = []
    for cat_articles in highlights.values():
        filtered_highlights.extend(cat_articles)
else:
    filtered_highlights = highlights.get(selected, [])

# Show articles
if filtered_highlights:
    st.markdown("### 🗂 Articles")
    for article in filtered_highlights:
        title = article.get("title", "No title")
        text = article.get("text") or article.get("summary") or "No article text available."
        url = article.get("url", "#")

        st.subheader(title)
        st.write(text[:500] + "...")
        st.write(f"URL: [Link]({url})")
        st.markdown("---")
else:
    st.write("No articles available in this category.")

# Ask the chatbot
st.markdown("## 🤖 Ask a Question About")

query = st.text_input("Enter your question here:")

if query and filtered_highlights:
    with st.spinner("Asking GroqCloud..."):
        top_articles = get_top_k_articles(query, filtered_highlights, k=3)
        context = "\n\n".join([
            (a.get("text") or a.get("summary") or "") for a in top_articles
        ])
        try:
            response = ask_groq(query, context)
        except Exception as e:
            response = f"❌ Error from GroqCloud: {e}"

    st.markdown("### 💬 Chatbot Response")
    st.write(response)