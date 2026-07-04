import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def report_writer_agent(due_diligence_data):
    print("\n Report Writer Agent is working...")
    try:
        if due_diligence_data.get("status") == "error":
            return {"status": "error", "error": "Due Diligence Agent failed"}

        company_name = due_diligence_data.get("company_name", "")
        industry = due_diligence_data.get("industry", "")
        due_diligence = due_diligence_data.get("due_diligence", "")
        sources = due_diligence_data.get("sources", [])

        sources_text = ""
        for i, source in enumerate(sources, 1):
            sources_text += f"{i}. {source['title']}\n   {source['url']}\n"

        print(f"   Writing report for: {company_name}")
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        You are a Senior M&A Intelligence Report Writer.
        Company: {company_name}
        Industry: {industry}
        Due Diligence Analysis: {due_diligence}

        Write a complete professional M&A Intelligence Report:

        # M&A INTELLIGENCE REPORT: {company_name}

        ## Executive Summary
        ## Company Overview
        ## Market Position & Competitive Landscape
        ## Financial Profile
        ## Strengths & Value Drivers
        ## Risk Assessment
        ## Growth Opportunities
        ## Acquisition Recommendation
        ## Due Diligence Checklist
        ## Sources
        {sources_text}

        Minimum 700 words. Professional tone.
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

        print("Report Writer Agent completed!")
        return {
            "company_name": company_name,
            "industry": industry,
            "report": response.text,
            "sources": sources,
            "status": "success"
        }

    except Exception as e:
        print(f"Report Writer Agent Error: {e}")
        return {
            "company_name": company_name,
            "industry": industry,
            "report": "",
            "sources": [],
            "status": "error",
            "error": str(e)
        }