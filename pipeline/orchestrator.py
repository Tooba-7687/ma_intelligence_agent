from agents.research_agent import research_agent
from agents.due_diligence_agent import due_diligence_agent
from agents.report_writer_agent import report_writer_agent
import os
from datetime import datetime

def run_pipeline(company_name: str, industry: str) -> dict:
    print("\n" + "="*50)
    print("🚀 M&A Intelligence Pipeline Started")
    print("="*50)
    print(f"🏢 Company  : {company_name}")
    print(f"🏭 Industry : {industry}")
    print("="*50)

    start_time = datetime.now()

    print("\n[1/3] Running Research Agent...")
    research_data = research_agent(company_name, industry)
    if research_data["status"] == "error":
        return {"status": "error", "step": "research", "error": research_data.get("error", "Unknown error")}

    print("\n[2/3] Running Due Diligence Agent...")
    dd_data = due_diligence_agent(research_data)
    if dd_data["status"] == "error":
        return {"status": "error", "step": "due_diligence", "error": dd_data.get("error", "Unknown error")}

    print("\n[3/3] Running Report Writer Agent...")
    final_output = report_writer_agent(dd_data)
    if final_output["status"] == "error":
        return {"status": "error", "step": "report_writer", "error": final_output.get("error", "Unknown error")}

    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    report_path = save_report(company_name=company_name, report=final_output["report"])

    print("\n" + "="*50)
    print("✅ Pipeline Completed Successfully!")
    print(f"⏱️  Time Taken : {duration} seconds")
    print(f"📄 Report Saved: {report_path}")
    print("="*50)

    return {
        "status": "success",
        "company_name": company_name,
        "industry": industry,
        "report": final_output["report"],
        "sources": final_output["sources"],
        "duration": duration,
        "report_path": report_path
    }


def save_report(company_name: str, report: str) -> str:
    try:
        os.makedirs("outputs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = company_name[:30].replace(" ", "_").replace("/", "_")
        filename = f"outputs/{clean_name}_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"M&A Intelligence Report\n")
            f.write(f"Company: {company_name}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            f.write(report)
        return filename
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")
        return ""