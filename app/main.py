from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/highlights")
def get_highlights():
    with open("data/highlights.json") as f:
        return json.load(f)