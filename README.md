**News Dashboard Chatbot**

A chatbot-enabled news dashboard app combining FastAPI backend and Streamlit frontend to aggregate, analyze, and interact with news articles.

**Demo**
**Application URL:** https://news-dashboard-chatbot-6hnxfyvwealalbbbb7vj7g.streamlit.app/

**GitHub Repository:** https://github.com/subhanaMQ/news-dashboard-chatbot

**Features**

✅ News scraping and aggregation from multiple Australian news sources

✅ Text summarization for concise news highlights

✅ Categorization of articles into Sports, Lifestyle, Music, and Finance

✅ Duplicate filtering (if implemented in `generate_highlights.py`)

✅ Prioritization of top highlights using keywords like “Breaking” or frequency across sources

✅ Semantic search using sentence embeddings (via SentenceTransformers)

✅ Retrieval-Augmented Generation (RAG)-based chatbot using GroqCloud (LLaMA 3 model)

✅ Chatbot answers user questions using relevant articles as context

✅ Streamlit-based dashboard UI to browse categorized news

✅ Each article shows title, author, source, summary, and link

✅ Easy setup with pre-generated `highlights.json`

✅ Optimized embedding caching for faster performance

**Installation & Setup**

**Clone this repo:**

git clone https://github.com/subhanaMQ/news-dashboard-chatbot.git

cd news-dashboard-chatbot

**Create and activate a Python virtual environment:**


python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install the required packages:**

pip install -r requirements.txt

**Running Locally**

**Run the backend and frontend in separate terminal windows/tabs:**

**Generate News Highlights**

python generate_highlights.py

**Start the backend API server:**

uvicorn app.main:app --reload

**Start the Streamlit frontend dashboard:**

streamlit run frontend/dashboard.py
