import streamlit as st
import pandas as pd
import plotly.express as px


def render_gaps_page(data):

    gaps = data.get("gaps", [])

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">RESEARCH INTELLIGENCE</div>
            <h1>Research Gaps</h1>
            <p>
                Identify unexplored areas, limitations, and opportunities
                discovered from the research literature.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "🎯 Demo Mode: Research gaps shown here are based on sample/mock data. "
        "AI-generated gap detection will be connected after backend integration."
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    total_gaps = len(gaps)
    total_evidence = sum(
        gap.get("evidence_count", 0)
        for gap in gaps
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Research Gaps",
            total_gaps
        )

    with col2:
        st.metric(
            "Supporting Evidence",
            total_evidence
        )

    with col3:
        st.metric(
            "Analysis Status",
            "Demo"
        )

    st.markdown("---")

    # ---------------------------------------------------------
    # GAP CARDS
    # ---------------------------------------------------------

    st.markdown("## 🎯 Identified Research Gaps")

    if not gaps:
        st.warning("No research gaps available.")
        return

    for index, gap in enumerate(gaps, start=1):

        title = gap.get("title", "Untitled Gap")
        description = gap.get(
            "description",
            "No description available."
        )
        evidence_count = gap.get(
            "evidence_count",
            0
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div style="display:flex;
                            justify-content:space-between;
                            align-items:center;">
                    <h3>Gap {index}: {title}</h3>
                    <div class="status-pill">
                        {evidence_count} Evidence Items
                    </div>
                </div>

                <p>{description}</p>

                <hr>

                <strong>Research Opportunity</strong>
                <p>
                    Further investigation in this area may help address
                    the limitation identified in the literature.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # EVIDENCE DISTRIBUTION
    # ---------------------------------------------------------

    st.markdown("## 📊 Evidence Distribution")

    gap_df = pd.DataFrame(
        {
            "Research Gap": [
                gap.get("title", "Unknown")
                for gap in gaps
            ],
            "Evidence": [
                gap.get("evidence_count", 0)
                for gap in gaps
            ]
        }
    )

    fig = px.bar(
        gap_df,
        x="Research Gap",
        y="Evidence",
        title="Evidence Supporting Each Research Gap"
    )

    fig.update_layout(
        xaxis_title="Research Gap",
        yaxis_title="Evidence Count",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------------------------
    # RESEARCH OPPORTUNITIES
    # ---------------------------------------------------------

    st.markdown("## 🚀 Potential Research Opportunities")

    opportunities = [
        (
            "Privacy-Preserving AI",
            "Explore approaches that allow healthcare AI systems "
            "to operate while reducing exposure of sensitive data."
        ),
        (
            "Explainable AI",
            "Investigate techniques that make AI predictions easier "
            "for researchers and end users to understand."
        ),
        (
            "Real-World Validation",
            "Study how AI models perform when deployed in realistic "
            "clinical environments."
        ),
        (
            "High-Quality Datasets",
            "Develop representative and reliable datasets for "
            "training and evaluating healthcare AI systems."
        )
    ]

    for title, description in opportunities:

        st.markdown(
            f"""
            <div class="info-card">
                <h3>🔬 {title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    st.markdown(
        """
        <div class="status-card">
            <div>
                <strong>Research Gap Analysis</strong><br>
                <span>
                    Gap identification is currently running with
                    demonstration data.
                </span>
            </div>

            <div class="status-pill">
                ● DEMO READY
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )