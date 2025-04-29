
# import json

# def fetch_all_articles():
#     articles = []
#     with open("news_data.jsonl", 'r', encoding='utf-8') as f:
#         for line in f:
#             articles.append(json.loads(line))
#     return sorted(articles, key=lambda x: x['content'], reverse=True)
