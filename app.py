# app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import HTMLResponse
import aiofiles
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NEWS_FILE = "news_data.jsonl"
STOP_WORDS = ["stop", "exit", "quit"]

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    async with aiofiles.open("index.html", mode="r") as f:
        return await f.read()

app.mount("/static", StaticFiles(directory="."), name="static")

def load_news():
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f][:5]

@app.get("/chat")
def chat(q: str = Query(..., description="User's voice command")):
    q_lower = q.lower()
    if any(word in q_lower for word in STOP_WORDS):
        return {"response": "Stopping. Have a nice day!"}
    if any(keyword in q_lower for keyword in ["news", "latest", "update", "headlines", "current"]):
        articles = load_news()
        message = "Here are the top news headlines. "
        for i, art in enumerate(articles, 1):
            message += f"News {i}: {art['title']}. {art['content'][:150]}... "
        return {"response": message}
    return {"response": "I'm a news assistant. I only provide the latest news updates."}
