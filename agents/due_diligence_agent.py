import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def due_diligence_agent(research_data):
    print("\n Due Diligence Agent is working...")
    try:
        if research_data.get("status") == "error":
            return {"status": "error", "error": "Research Agent failed"}

        company_name = research_data.get("company_name", "")
        industry = research_data.get("industry", "")
        raw_data = research_data.get("raw_data", "")

        print(f"   Analyzing: {company_name}")
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a Senior M&A Due Diligence Analyst.
        Company: {company_name}
        Industry: {industry}
        Research Data: {raw_data}

        Provide structured analysis:
        ACQUISITION ATTRACTIVENESS SCORE: (1-10)
        STRENGTHS: (list key strengths)
        RED FLAGS & RISKS: (list concerns)
        OPPORTUNITIES: (list growth opportunities)
        VALUATION SIGNALS: (revenue indicators)
        RECOMMENDED NEXT STEPS: (what buyer should investigate)
        OVERALL VERDICT: (Buy / Watch / Pass with reasoning)
        """

        response = None
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                break
            except Exception as api_err:
                if "429" in str(api_err) and attempt < 2:
                    wait = 5 * (attempt + 1)
                    print(f"   Rate limited, retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise

        print("Due Diligence Agent completed!")
        return {
            "company_name": company_name,
            "industry": industry,
            "due_diligence": response.text,
            "sources": research_data.get("sources", []),
            "status": "success"
        }

    except Exception as e:
        print(f"Due Diligence Agent Error: {e}")
        return {
            "company_name": company_name,
            "industry": industry,
            "due_diligence": "",
            "sources": [],
            "status": "error",
            "error": str(e)
        }