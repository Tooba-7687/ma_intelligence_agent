import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



import sys
sys.path.insert(0, r"C:\Ai Agents\ma_intelligence_agent")
from pipeline.orchestrator import run_pipeline

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title = "M&A Intelligence Agent",
    page_icon  = "🏢",
    layout     = "wide"
)

# ─────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────
st.markdown("""
    <style>
    :root {
        color-scheme: dark;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #07111f 0%, #111827 45%, #172338 100%);
    }

    .stApp {
        color: #f8fafc;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #f8fafc;
        text-align: center;
        padding: 1rem 0 0.4rem;
        letter-spacing: 0.02em;
        text-shadow: 0 2px 12px rgba(56, 189, 248, 0.2);
    }

    .subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 1.6rem;
    }

    .agent-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-left: 4px solid #38bdf8;
        padding: 1rem 1.1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 8px 24px rgba(2, 6, 23, 0.25);
        backdrop-filter: blur(8px);
    }

    .agent-card h4 {
        color: #f8fafc;
        margin: 0 0 0.45rem 0;
        font-size: 1.05rem;
    }

    .agent-card p {
        color: #cbd5e1;
        margin: 0;
        line-height: 1.5;
    }

    .success-box {
        background: rgba(22, 101, 52, 0.2);
        border: 1px solid rgba(74, 222, 128, 0.45);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dcfce7;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
    }

    .error-box {
        background: rgba(127, 29, 29, 0.2);
        border: 1px solid rgba(248, 113, 113, 0.45);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffe4e6;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(15, 23, 42, 0.9);
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 8px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1.1rem;
        font-weight: 700;
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(56, 189, 248, 0.32);
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #f8fafc;
    }

    .stMarkdown p, .stMarkdown li {
        color: #e2e8f0;
    }

    div[data-testid="stHorizontalBlock"] > div {
        gap: 0.7rem;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown('<div class="main-title">🏢 M&A Intelligence Agent</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Google Gemini + Tavily Search | 3 AI Agents working together</div>',
            unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# AGENT OVERVIEW
# ─────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Research Agent</h4>
        <p>Searches the web & extracts company data using Tavily</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <h4>🔎 Due Diligence Agent</h4>
        <p>Analyzes company from M&A buyer/investor perspective</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <h4>✍️ Report Writer Agent</h4>
        <p>Writes a professional M&A Intelligence Report</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────
st.subheader("🏢 Enter Company Details")

col_company, col_industry = st.columns(2)

with col_company:
    company_name = st.text_input(
        label       = "Company Name",
        placeholder = "e.g. Stripe, Airbnb, Careem"
    )

with col_industry:
    industry = st.text_input(
        label       = "Industry",
        placeholder = "e.g. FinTech, SaaS, E-commerce"
    )

run_button = st.button(
    "🚀 Generate M&A Report",
    use_container_width = True,
    type = "primary"
)

st.divider()

# ─────────────────────────────────────────
# PIPELINE EXECUTION
# ─────────────────────────────────────────
if run_button:
    if not company_name.strip() or not industry.strip():
        st.error("⚠️ Please enter both Company Name and Industry!")
    else:
        st.subheader("⚙️ Pipeline Running...")
        progress_bar = st.progress(0)
        status_text  = st.empty()

        with st.spinner("🤖 Agents are working..."):
            status_text.text("🔍 Research Agent searching the web...")
            progress_bar.progress(10)

            result = run_pipeline(
                company_name = company_name,
                industry     = industry
            )

            progress_bar.progress(100)
            status_text.text("✅ All agents completed!")

        st.divider()

        if result["status"] == "success":
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>M&A Report Generated!</strong>
                &nbsp;|&nbsp; ⏱️ Time: {result['duration']} seconds
                &nbsp;|&nbsp; 🏢 Company: {result['company_name']}
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📄 M&A Intelligence Report")
            st.markdown(result["report"])

            st.divider()

            if result["sources"]:
                st.subheader("🔗 Sources Used")
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"{i}. [{source['title']}]({source['url']})")

            st.divider()

            st.download_button(
                label     = "⬇️ Download Report as .txt",
                data      = result["report"],
                file_name = f"MA_Report_{company_name[:20].replace(' ','_')}.txt",
                mime      = "text/plain"
            )

        else:
            st.markdown(f"""
            <div class="error-box">
                ❌ <strong>Pipeline Failed</strong>
                at step: <strong>{result.get('step', 'unknown')}</strong><br>
                Error: {result.get('error', 'Unknown error')}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("""
    <div style='text-align:center; color:#888; font-size:0.85rem;'>
        Built by Tooba Nadeem &nbsp;|&nbsp;
        M&A Intelligence Agent &nbsp;|&nbsp;
        Powered by Gemini + Tavily
    </div>
""", unsafe_allow_html=True)