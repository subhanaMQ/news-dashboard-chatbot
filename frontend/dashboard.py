import streamlit as st
import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="News Dashboard + Chatbot", layout="wide")

# GroqCloud API info (replace with your actual key)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"

@st.cache_data
def load_highlights():
    with open("data/highlights.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def run_groq_query(question, context):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions about news articles."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    data = {
        "model": GROQ_MODEL,
        "messages": messages
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def find_similar_articles(question, articles, article_embeddings, embedding_model, top_n=3):
    question_emb = embedding_model.encode([question])
    similarities = cosine_similarity(question_emb, article_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    return [articles[i] for i in top_indices]

def main():
    st.title("📰 News Dashboard + Chatbot")

    highlights = load_highlights()
    embedding_model = load_embedding_model()

    # Flatten articles list, add category key
    all_articles = []
    for category, arts in highlights.items():
        for art in arts:
            art['category'] = category
            all_articles.append(art)

    # Prepare text for embeddings (summary or title fallback)
    texts = [art.get("summary") or art.get("title") or "" for art in all_articles]
    article_embeddings = embedding_model.encode(texts, show_progress_bar=False)

    tab1, tab2 = st.tabs(["Highlights", "Ask News Bot"])

    with tab1:
        st.header("News Highlights by Category")
        for category, arts in highlights.items():
            with st.expander(f"{category.capitalize()} ({len(arts)} articles)"):
                for art in arts:
                    title = art.get("title", "No title")
                    author = art.get("author", "Unknown author")
                    source = art.get("source", "Unknown source")
                    summary = art.get("summary") or art.get("text") or "No summary available."
                    url = art.get("url", "#")

                    st.markdown(f"### {title}")
                    st.markdown(f"**Source:** {source} | **Author:** {author}")
                    st.markdown(summary)
                    st.markdown(f"[Read full article]({url})")
                    st.markdown("---")

    with tab2:
        st.header("Ask questions about the news")
        user_question = st.text_input("Enter your question here:")

        if st.button("Ask") and user_question.strip():
            with st.spinner("Searching relevant articles and querying GroqCloud..."):
                similar_articles = find_similar_articles(
                    user_question, all_articles, article_embeddings, embedding_model, top_n=3
                )

                context = "\n\n".join(
                    f"Title: {a.get('title')}\nSummary: {a.get('summary') or a.get('text')}\nURL: {a.get('url')}"
                    for a in similar_articles
                )

                try:
                    answer = run_groq_query(user_question, context)
                except Exception as e:
                    answer = f"Error calling GroqCloud API: {e}"

            st.markdown("### Answer:")
            st.write(answer)

if __name__ == "__main__":
    main()