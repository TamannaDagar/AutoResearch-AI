import streamlit as st


def render_literature_review_page(data):

    review = data.get("literature_review", {})

    introduction = review.get("introduction", "")
    methodology = review.get("methodology", "")
    themes = review.get("themes", [])
    future_directions = review.get("future_directions", [])

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">RESEARCH SYNTHESIS</div>
            <h1>Literature Review</h1>
            <p>
                A structured synthesis of the research literature,
                major themes, and potential future directions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "📝 Demo Mode: This literature review is generated from "
        "sample/mock research data. AI-generated synthesis will be "
        "connected after backend integration."
    )

    # ---------------------------------------------------------
    # INTRODUCTION
    # ---------------------------------------------------------

    st.markdown("## 📖 Introduction")

    st.markdown(
        f"""
        <div class="info-card">
            <p>{introduction}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------------
    # METHODOLOGY
    # ---------------------------------------------------------

    st.markdown("## 🔬 Review Methodology")

    st.markdown(
        f"""
        <div class="info-card">
            <p>{methodology}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------------------------------
    # MAJOR THEMES
    # ---------------------------------------------------------

    st.markdown("## 🧠 Major Research Themes")

    if themes:

        cols = st.columns(2)

        for index, theme in enumerate(themes):

            with cols[index % 2]:

                st.markdown(
                    f"""
                    <div class="info-card">
                        <h3>🔹 {theme}</h3>
                        <p>
                            This theme represents an important area
                            within the selected research literature.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ---------------------------------------------------------
    # FUTURE DIRECTIONS
    # ---------------------------------------------------------

    st.markdown("## 🚀 Future Research Directions")

    for index, direction in enumerate(
        future_directions,
        start=1
    ):

        st.markdown(
            f"""
            <div class="info-card">
                <h3>Direction {index}</h3>
                <p>{direction}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # GENERATE REVIEW PLACEHOLDER
    # ---------------------------------------------------------

    st.markdown("## ✨ Literature Review Generator")

    st.markdown(
        """
        <div class="status-card">
            <div>
                <strong>AI Literature Synthesis</strong><br>
                <span>
                    The final AI-generated literature review will be
                    produced from retrieved papers and verified evidence.
                </span>
            </div>

            <div class="status-pill">
                ● BACKEND PENDING
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✨ Generate Literature Review",
        use_container_width=True
    ):
        st.info(
            "Demo Mode: Literature review generation will be enabled "
            "after the backend AI pipeline is connected."
        )