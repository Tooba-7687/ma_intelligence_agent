import google.generativeai as genai
from tools.web_search import search_web, format_search_results
from dotenv import load_dotenv
import os
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def research_agent(company_name: str, industry: str) -> dict:
    print("\n🔍 Research Agent is working...")
    print(f"   Company: {company_name} | Industry: {industry}")
    try:
        query = f"{company_name} {industry} company revenue employees market position news 2024 2025"
        print("   Searching the web...")
        raw_results = search_web(query, max_results=5)
        formatted_results = format_search_results(raw_results)

        print("   Extracting key information with Gemini...")
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        You are an M&A Research Agent. Analyze these web search results 
        about {company_name} in the {industry} industry.
        Web Search Results:
        {formatted_results}
        Extract and structure:
        1. Company Overview
        2. Financial Indicators
        3. Team & Scale
        4. Market Position
        5. Recent News
        6. Digital Presence
        Be factual. Only use information from search results.
        """
        response = None
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                break
            except Exception as api_err:
                if "429" in str(api_err) and attempt < 2:
                    wait = 5 * (attempt + 1)
                    print(f"   ⏳ Rate limited, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise

        sources = [{"title": r["title"], "url": r["url"]} for r in raw_results]
        print("✅ Research Agent completed!")
        return {
            "company_name": company_name,
            "industry": industry,
            "raw_data": response.text,
            "sources": sources,
            "status": "success"
        }
    except Exception as e:
        print(f"❌ Research Agent Error: {e}")
        return {
            "company_name": company_name,
            "industry": industry,
            "raw_data": "",
            "sources": [],
            "status": "error",
            "error": str(e)
        }