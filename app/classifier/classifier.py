from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

CATEGORIES = ["sports", "lifestyle", "music", "finance", "technology", "politics", "crime", "environment"]

def classify_article(text):
    result = classifier(text, CATEGORIES)
    return result["labels"][0]