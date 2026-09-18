import streamlit as st
import pandas as pd
import plotly.express as px


def render_trends_page(data):

    trends = data.get("trends", {})
    keywords = data.get("keywords", [])

    years = trends.get("years", [])
    paper_count = trends.get("paper_count", [])
    citation_count = trends.get("citation_count", [])

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">RESEARCH INTELLIGENCE</div>
            <h1>Research Trends</h1>
            <p>
                Explore publication growth, citation trends, and frequently
                researched topics across the selected research area.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "📊 Demo Mode: These charts currently use sample/mock research data. "
        "Real research trends will be connected after backend integration."
    )

    # ---------------------------------------------------------
    # SUMMARY METRICS
    # ---------------------------------------------------------

    latest_papers = paper_count[-1] if paper_count else 0
    latest_citations = citation_count[-1] if citation_count else 0

    first_papers = paper_count[0] if paper_count else 0

    if first_papers > 0:
        growth = ((latest_papers - first_papers) / first_papers) * 100
    else:
        growth = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latest Papers",
            latest_papers
        )

    with col2:
        st.metric(
            "Latest Citations",
            latest_citations
        )

    with col3:
        st.metric(
            "Publication Growth",
            f"{growth:.1f}%"
        )

    st.markdown("---")

    # ---------------------------------------------------------
    # PAPERS OVER YEARS
    # ---------------------------------------------------------

    st.markdown("## 📚 Publications Over Time")

    papers_df = pd.DataFrame(
        {
            "Year": years,
            "Papers": paper_count
        }
    )

    if not papers_df.empty:

        fig_papers = px.line(
            papers_df,
            x="Year",
            y="Papers",
            markers=True,
            title="Research Paper Growth"
        )

        fig_papers.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Papers",
            height=420
        )

        st.plotly_chart(
            fig_papers,
            use_container_width=True
        )

    # ---------------------------------------------------------
    # CITATIONS OVER YEARS
    # ---------------------------------------------------------

    st.markdown("## 📈 Citation Trends")

    citations_df = pd.DataFrame(
        {
            "Year": years,
            "Citations": citation_count
        }
    )

    if not citations_df.empty:

        fig_citations = px.bar(
            citations_df,
            x="Year",
            y="Citations",
            title="Citation Growth Over Time"
        )

        fig_citations.update_layout(
            xaxis_title="Year",
            yaxis_title="Citation Count",
            height=420
        )

        st.plotly_chart(
            fig_citations,
            use_container_width=True
        )

    # ---------------------------------------------------------
    # KEYWORD FREQUENCY
    # ---------------------------------------------------------

    st.markdown("## 🔑 Research Keyword Frequency")

    keyword_df = pd.DataFrame(keywords)

    if not keyword_df.empty:

        keyword_df = keyword_df.sort_values(
            "frequency",
            ascending=True
        )

        fig_keywords = px.bar(
            keyword_df,
            x="frequency",
            y="keyword",
            orientation="h",
            title="Most Frequently Used Research Keywords"
        )

        fig_keywords.update_layout(
            xaxis_title="Frequency",
            yaxis_title="Keyword",
            height=450
        )

        st.plotly_chart(
            fig_keywords,
            use_container_width=True
        )

    # ---------------------------------------------------------
    # TREND INSIGHTS
    # ---------------------------------------------------------

    st.markdown("## 💡 Trend Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.markdown(
            """
            <div class="info-card">
                <h3>📊 Publication Growth</h3>
                <p>
                    The number of research papers shows a continuous increase
                    across the selected years, indicating growing research
                    activity in the topic.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col2:

        st.markdown(
            """
            <div class="info-card">
                <h3>🔍 Dominant Topics</h3>
                <p>
                    Artificial Intelligence, Machine Learning and Deep Learning
                    appear among the most frequently represented research areas
                    in the demo dataset.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="status-card">
            <div>
                <strong>Trend Analysis Status</strong><br>
                <span>Charts generated successfully from mock research data.</span>
            </div>
            <div class="status-pill">● DEMO READY</div>
        </div>
        """,
        unsafe_allow_html=True
    )