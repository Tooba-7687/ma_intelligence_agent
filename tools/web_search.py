from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

def search_web(query, max_results=5):
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results
        )
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")
            })
        return results
    except Exception as e:
        print(f"Search Error: {e}")
        return []


def format_search_results(results):
    if not results:
        return "No results found."
    formatted = ""
    for i, result in enumerate(results, 1):
        formatted += f"\n--- Result {i} ---\n"
        formatted += f"Title:   {result['title']}\n"
        formatted += f"URL:     {result['url']}\n"
        formatted += f"Content: {result['content']}\n"
    return formatted