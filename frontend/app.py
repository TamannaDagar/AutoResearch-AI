import json
from pathlib import Path

import streamlit as st

from components.sidebar import render_sidebar
from pages.papers import render_papers_page
from pages.analysis import render_analysis_page
from pages.evidence import render_evidence_page
from pages.trends import render_trends_page
from pages.gaps import render_gaps_page
from pages.literature_review import render_literature_review_page
from pages.report import render_report_page

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoResearch AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD MOCK DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "mock_data" / "sample_data.json"


def load_mock_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


data = load_mock_data()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #0F172A;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    .sidebar-brand {
        text-align: center;
        padding: 10px 5px 25px 5px;
    }

    .brand-icon {
        font-size: 38px;
        margin-bottom: 5px;
    }

    .brand-name {
        font-size: 21px;
        font-weight: 750;
        color: #1D4ED8;
    }

    .brand-subtitle {
        font-size: 11px;
        color: #64748B;
        margin-top: 5px;
    }

    .sidebar-section-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #94A3B8;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .status-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 12px;
    }

    .status-title {
        font-size: 11px;
        font-weight: 700;
        color: #15803D;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        background-color: #22C55E;
        border-radius: 50%;
        margin-right: 5px;
    }

    .status-description {
        font-size: 11px;
        color: #64748B;
        margin-top: 5px;
        line-height: 1.4;
    }

    .sidebar-footer {
        padding-top: 15px;
        border-top: 1px solid #E2E8F0;
    }

    .footer-title {
        font-size: 12px;
        font-weight: 650;
        color: #334155;
    }

    .footer-text {
        font-size: 10px;
        color: #94A3B8;
        margin-top: 3px;
    }


    /* =====================================================
       HERO SECTION
       ===================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #EFF6FF 0%,
            #FFFFFF 55%,
            #F8FAFC 100%
        );

        border: 1px solid #DBEAFE;

        border-radius: 18px;

        padding: 38px;

        margin-bottom: 25px;
    }

    .hero-badge {
        display: inline-block;

        background-color: #DBEAFE;

        color: #1D4ED8;

        padding: 6px 12px;

        border-radius: 20px;

        font-size: 12px;

        font-weight: 700;

        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 42px;

        font-weight: 800;

        color: #0F172A;

        margin-bottom: 10px;
    }

    .hero-description {
        font-size: 16px;

        color: #64748B;

        max-width: 800px;

        line-height: 1.6;
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {
        font-size: 22px;

        font-weight: 750;

        color: #0F172A;

        margin-top: 28px;

        margin-bottom: 15px;
    }


    /* =====================================================
       KPI CARDS
       ===================================================== */

    .kpi-card {
        background-color: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 20px;

        min-height: 125px;

        box-shadow:
            0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .kpi-label {
        font-size: 12px;

        color: #64748B;

        font-weight: 600;

        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 28px;

        font-weight: 800;

        color: #0F172A;
    }

    .kpi-description {
        font-size: 11px;

        color: #94A3B8;

        margin-top: 5px;
    }


    /* =====================================================
       WORKFLOW
       ===================================================== */

    .workflow-card {
        background-color: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 20px;

        height: 100%;
    }

    .workflow-number {
        font-size: 12px;

        font-weight: 700;

        color: #2563EB;
    }

    .workflow-title {
        font-size: 14px;

        font-weight: 700;

        color: #0F172A;

        margin-top: 6px;
    }

    .workflow-description {
        font-size: 11px;

        color: #64748B;

        line-height: 1.5;

        margin-top: 5px;
    }


    /* =====================================================
       RESEARCH OVERVIEW
       ===================================================== */

    .overview-card {
        background-color: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 22px;
    }

    .overview-label {
        font-size: 11px;

        color: #94A3B8;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.7px;
    }

    .overview-value {
        font-size: 18px;

        font-weight: 700;

        color: #0F172A;

        margin-top: 5px;
    }


    /* =====================================================
       SYSTEM STATUS
       ===================================================== */

    .system-card {
        background-color: #FFFFFF;

        border: 1px solid #E2E8F0;

        border-radius: 14px;

        padding: 18px;
    }

    .system-row {
        display: flex;

        justify-content: space-between;

        padding: 10px 0;

        border-bottom: 1px solid #F1F5F9;

        font-size: 13px;
    }

    .system-row:last-child {
        border-bottom: none;
    }

    .system-name {
        color: #475569;
    }

    .system-status {
        color: #15803D;

        font-weight: 700;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

selected_page = render_sidebar()


# ============================================================
# HOME PAGE
# ============================================================

if selected_page == "🏠 Home":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero">

            <div class="hero-badge">
                🔬 AI-POWERED RESEARCH PLATFORM
            </div>

            <div class="hero-title">
                AutoResearch AI
            </div>

            <div class="hero-description">
                Discover research papers, analyze academic literature,
                identify research trends and uncover research gaps
                with an intelligent research analysis platform.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # RESEARCH TOPIC
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Start Your Research</div>',
        unsafe_allow_html=True
    )

    topic_col, button_col = st.columns([5, 1])

    with topic_col:

        research_topic = st.text_input(
            "Research Topic",
            value=data["research_topic"],
            placeholder="Enter your research topic...",
            label_visibility="collapsed"
        )

    with button_col:

        start_research = st.button(
            "🚀 Start Research",
            use_container_width=True
        )

    if start_research:

        st.success(
            f"Research initialized for: {research_topic}"
        )

        st.info(
            "Demo mode: backend processing is not connected yet. "
            "This frontend currently uses mock research data."
        )


    # --------------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Research Overview</div>',
        unsafe_allow_html=True
    )

    summary = data["summary"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    📚 PAPERS FOUND
                </div>

                <div class="kpi-value">
                    {summary["papers_found"]}
                </div>

                <div class="kpi-description">
                    Research papers discovered
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    📊 CITATIONS
                </div>

                <div class="kpi-value">
                    {summary["citations"]:,}
                </div>

                <div class="kpi-description">
                    Total citations in dataset
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    🔓 OPEN ACCESS
                </div>

                <div class="kpi-value">
                    {summary["open_access"]}
                </div>

                <div class="kpi-description">
                    Papers with open access
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    🎯 RESEARCH GAPS
                </div>

                <div class="kpi-value">
                    {summary["research_gaps"]}
                </div>

                <div class="kpi-description">
                    Potential gaps identified
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Research Intelligence Workflow</div>',
        unsafe_allow_html=True
    )

    workflow = [
        (
            "01",
            "Paper Discovery",
            "Find relevant academic papers from research sources."
        ),
        (
            "02",
            "PDF Processing",
            "Retrieve, extract and clean research paper content."
        ),
        (
            "03",
            "Semantic Search",
            "Search research content using vector embeddings."
        ),
        (
            "04",
            "AI Analysis",
            "Analyze literature using intelligent research agents."
        ),
        (
            "05",
            "Research Insights",
            "Identify trends, gaps, evidence and future directions."
        )
    ]

    workflow_cols = st.columns(5)

    for index, item in enumerate(workflow):

        number, title, description = item

        with workflow_cols[index]:

            st.markdown(
                f"""
                <div class="workflow-card">

                    <div class="workflow-number">
                        STEP {number}
                    </div>

                    <div class="workflow-title">
                        {title}
                    </div>

                    <div class="workflow-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # CURRENT RESEARCH + SYSTEM STATUS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Current Research</div>',
        unsafe_allow_html=True
    )

    research_col, system_col = st.columns([1.5, 1])

    with research_col:

        st.markdown(
            f"""
            <div class="overview-card">

                <div class="overview-label">
                    Research Topic
                </div>

                <div class="overview-value">
                    {data["research_topic"]}
                </div>

                <br>

                <div class="overview-label">
                    Analysis Status
                </div>

                <div class="overview-value">
                    {summary["analysis_status"]}
                </div>

                <br>

                <div class="overview-label">
                    Papers Available
                </div>

                <div class="overview-value">
                    {summary["papers_found"]} papers
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with system_col:

        st.markdown(
            """
            <div class="system-card">

                <div class="system-row">
                    <span class="system-name">
                        Frontend
                    </span>

                    <span class="system-status">
                        ● Active
                    </span>
                </div>

                <div class="system-row">
                    <span class="system-name">
                        Mock Data
                    </span>

                    <span class="system-status">
                        ● Active
                    </span>
                </div>

                <div class="system-row">
                    <span class="system-name">
                        Backend API
                    </span>

                    <span class="system-status">
                        ● Not Connected
                    </span>
                </div>

                <div class="system-row">
                    <span class="system-name">
                        Vector Database
                    </span>

                    <span class="system-status">
                        ● Not Connected
                    </span>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )
        
        
        
# ============================================================
# OTHER PAGES
# ============================================================

if selected_page == "📚 Papers":

    render_papers_page(data)
    
if selected_page == "🧠 Analysis":
    
    render_analysis_page(data)
    
if selected_page == "🔎 Evidence":
    
    render_evidence_page(data)
    
if selected_page == "📈 Trends":
    render_trends_page(data)
    
if selected_page == "🎯 Research Gaps":
    render_gaps_page(data)
    
if selected_page == "📝 Literature Review":
    render_literature_review_page(data)
    
if selected_page == "📄 Report":
    render_report_page(data)