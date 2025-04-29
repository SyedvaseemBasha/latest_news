
# from fastapi import FastAPI
# import json
# import pyttsx3
# import threading
# from llm_utils import rephrase_content
# from fetch_news import fetch_all_articles

# app = FastAPI()

# @app.get("/latestnews")
# def speak_latest_news():
#     articles = fetch_all_articles()
#     top_contents = [a['content'] for a in articles[:5] if a.get('content')]

#     def speak(news_list):
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 150)
#         for idx, news in enumerate(news_list, 1):
#             engine.say(f"News {idx}: {news}")
#             engine.runAndWait()

#     thread = threading.Thread(target=speak, args=(top_contents,))
#     thread.start()
#     return {"status": "Speaking top 5 news in background."}

# app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

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

# Load JSONL news articles
def load_news():
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f][:5]  # Top 5 only

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

