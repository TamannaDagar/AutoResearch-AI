import streamlit as st
import plotly.express as px


def render_analysis_page(data):
    """
    Displays the research analysis dashboard.
    Uses mock data until the backend AI pipeline is connected.
    """

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🧠 Research Analysis")

    st.markdown(
        "Analyze the collected literature, identify major themes, "
        "and review key findings from the research dataset."
    )

    st.divider()

    # ========================================================
    # ANALYSIS DATA
    # ========================================================

    analysis = data.get("analysis", {})

    summary = analysis.get(
        "summary",
        "No research summary available."
    )

    key_findings = analysis.get(
        "key_findings",
        []
    )

    themes = analysis.get(
        "themes",
        []
    )

    # ========================================================
    # AI STATUS
    # ========================================================

    st.info(
        "🤖 Demo Analysis Mode — These insights are generated "
        "from the current mock dataset. AI backend integration "
        "will be added later."
    )

    # ========================================================
    # RESEARCH SUMMARY
    # ========================================================

    st.subheader("📋 Research Summary")

    st.markdown(
        f"""
        <div style="
            background-color: white;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 22px;
            line-height: 1.7;
            color: #475569;
            font-size: 14px;
        ">
            {summary}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # KEY FINDINGS
    # ========================================================

    st.subheader("🔍 Key Findings")

    if key_findings:

        finding_cols = st.columns(2)

        for index, finding in enumerate(key_findings):

            with finding_cols[index % 2]:

                st.markdown(
                    f"""
                    <div style="
                        background-color: white;
                        border: 1px solid #E2E8F0;
                        border-radius: 14px;
                        padding: 18px;
                        margin-bottom: 15px;
                        min-height: 90px;
                    ">

                        <div style="
                            font-size: 12px;
                            font-weight: 700;
                            color: #2563EB;
                            margin-bottom: 7px;
                        ">
                            FINDING {index + 1}
                        </div>

                        <div style="
                            font-size: 14px;
                            color: #334155;
                            line-height: 1.5;
                        ">
                            {finding}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("No key findings available.")

    # ========================================================
    # RESEARCH THEMES
    # ========================================================

    st.subheader("🧩 Research Themes")

    if themes:

        theme_names = [
            theme.get("name", "Unknown")
            for theme in themes
        ]

        theme_counts = [
            theme.get("paper_count", 0)
            for theme in themes
        ]

        # ----------------------------------------------------
        # CREATE DATAFRAME
        # ----------------------------------------------------

        import pandas as pd

        theme_df = pd.DataFrame(
            {
                "Theme": theme_names,
                "Papers": theme_counts
            }
        )

        # ----------------------------------------------------
        # PLOTLY CHART
        # ----------------------------------------------------

        fig = px.bar(
            theme_df,
            x="Theme",
            y="Papers",
            title="Research Papers by Major Theme",
            text="Papers"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            height=450,
            xaxis_title="Research Theme",
            yaxis_title="Number of Papers",
            margin=dict(
                l=20,
                r=20,
                t=70,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # THEME TABLE
        # ----------------------------------------------------

        st.markdown("### Theme Breakdown")

        st.dataframe(
            theme_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No research theme data available.")

    # ========================================================
    # ANALYSIS INSIGHTS
    # ========================================================

    st.subheader("💡 Analysis Insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:

        st.markdown(
            """
            <div style="
                background-color: #EFF6FF;
                border: 1px solid #DBEAFE;
                border-radius: 12px;
                padding: 18px;
            ">

                <div style="
                    font-size: 22px;
                ">
                    📚
                </div>

                <div style="
                    font-weight: 700;
                    color: #1E3A8A;
                    margin-top: 8px;
                ">
                    Literature Coverage
                </div>

                <div style="
                    font-size: 12px;
                    color: #64748B;
                    margin-top: 5px;
                    line-height: 1.5;
                ">
                    Multiple research themes are represented
                    in the current literature dataset.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col2:

        st.markdown(
            """
            <div style="
                background-color: #F0FDF4;
                border: 1px solid #BBF7D0;
                border-radius: 12px;
                padding: 18px;
            ">

                <div style="
                    font-size: 22px;
                ">
                    🧠
                </div>

                <div style="
                    font-weight: 700;
                    color: #166534;
                    margin-top: 8px;
                ">
                    Dominant Research
                </div>

                <div style="
                    font-size: 12px;
                    color: #64748B;
                    margin-top: 5px;
                    line-height: 1.5;
                ">
                    Machine learning and deep learning
                    appear prominently in the dataset.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col3:

        st.markdown(
            """
            <div style="
                background-color: #FFF7ED;
                border: 1px solid #FED7AA;
                border-radius: 12px;
                padding: 18px;
            ">

                <div style="
                    font-size: 22px;
                ">
                    🎯
                </div>

                <div style="
                    font-weight: 700;
                    color: #9A3412;
                    margin-top: 8px;
                ">
                    Further Investigation
                </div>

                <div style="
                    font-size: 12px;
                    color: #64748B;
                    margin-top: 5px;
                    line-height: 1.5;
                ">
                    Research gaps and evidence should be
                    investigated before drawing final conclusions.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )