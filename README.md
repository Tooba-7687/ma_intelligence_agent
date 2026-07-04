# M&A Intelligence Agent

A Streamlit-based AI application that generates M&A intelligence reports using multiple specialized agents.

## Features

- Research agent gathers company and market information
- Due diligence agent analyzes the company from an M&A perspective
- Report writer agent creates a polished intelligence report
- Includes source links and downloadable report output

## Tech Stack

- Python
- Streamlit
- Google Gemini
- Tavily Search

## Project Structure

- agents/ - AI agents for research, diligence, and report writing
- pipeline/ - orchestration logic for the full workflow
- tools/ - search and utility integrations
- ui/ - Streamlit app interface

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run ui/app.py
```

## Environment Variables

Make sure you set any required API keys for Gemini and Tavily before running the app.

## Notes

This project is designed for generating structured M&A research summaries and can be extended with additional analysis modules.
