import streamlit as st


def render_sidebar():
    """
    Creates the main navigation sidebar
    and returns the currently selected page.
    """

    with st.sidebar:

        # -----------------------------------------
        # BRANDING
        # -----------------------------------------

        st.markdown(
            """
            <div class="sidebar-brand">

                <div class="brand-icon">
                    🔬
                </div>

                <div class="brand-name">
                    AutoResearch AI
                </div>

                <div class="brand-subtitle">
                    AI-Powered Research Assistant
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------
        # NAVIGATION
        # -----------------------------------------

        st.markdown(
            '<div class="sidebar-section-title">RESEARCH</div>',
            unsafe_allow_html=True
        )

        selected_page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "📚 Papers",
                "🧠 Analysis",
                "🔎 Evidence",
                "📈 Trends",
                "🎯 Research Gaps",
                "📝 Literature Review",
                "📄 Report"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        # -----------------------------------------
        # PROJECT STATUS
        # -----------------------------------------

        st.markdown(
            '<div class="sidebar-section-title">PROJECT</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="status-card">

                <div class="status-title">
                    <span class="status-dot"></span>
                    MOCK DATA MODE
                </div>

                <div class="status-description">
                    Frontend is currently running
                    with sample research data.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        # -----------------------------------------
        # PROJECT INFORMATION
        # -----------------------------------------

        st.markdown(
            """
            <div class="sidebar-footer">

                <div class="footer-title">
                    AutoResearch AI
                </div>

                <div class="footer-text">
                    B.Tech Final Year Project
                </div>

                <div class="footer-text">
                    Research Intelligence Platform
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    return selected_page