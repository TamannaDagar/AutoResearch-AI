import streamlit as st


def render_papers_page(data):
    """
    Displays the research papers dashboard.
    Uses mock data for now.
    """

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("📚 Research Papers")

    st.markdown(
        "Explore, search and filter the academic papers "
        "collected for your research topic."
    )

    st.divider()

    # ========================================================
    # PAPER DATA
    # ========================================================

    papers = data.get("papers", [])

    if not papers:
        st.warning("No research papers available.")
        return

    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    total_papers = len(papers)

    open_access = sum(
        1 for paper in papers
        if paper.get("open_access", False)
    )

    pdf_available = sum(
        1 for paper in papers
        if paper.get("pdf_available", False)
    )

    total_citations = sum(
        paper.get("citations", 0)
        for paper in papers
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "📚 Papers",
            total_papers
        )

    with metric2:
        st.metric(
            "🔓 Open Access",
            open_access
        )

    with metric3:
        st.metric(
            "📄 PDF Available",
            pdf_available
        )

    with metric4:
        st.metric(
            "📊 Citations",
            f"{total_citations:,}"
        )

    st.markdown("")

    # ========================================================
    # FILTERS
    # ========================================================

    st.subheader("Search & Filters")

    filter1, filter2, filter3 = st.columns([2, 1, 1])

    with filter1:

        search_query = st.text_input(
            "Search papers",
            placeholder="Search by title, author or DOI..."
        )

    with filter2:

        years = sorted(
            {
                paper.get("year")
                for paper in papers
                if paper.get("year") is not None
            },
            reverse=True
        )

        selected_year = st.selectbox(
            "Year",
            ["All Years"] + years
        )

    with filter3:

        access_filter = st.selectbox(
            "Access",
            [
                "All Papers",
                "Open Access",
                "Not Open Access"
            ]
        )

    # ========================================================
    # FILTER LOGIC
    # ========================================================

    filtered_papers = papers.copy()

    # Search filter
    if search_query:

        query = search_query.lower().strip()

        filtered_papers = [
            paper
            for paper in filtered_papers
            if (
                query in paper.get("title", "").lower()
                or query in " ".join(
                    paper.get("authors", [])
                ).lower()
                or query in paper.get("doi", "").lower()
            )
        ]

    # Year filter
    if selected_year != "All Years":

        filtered_papers = [
            paper
            for paper in filtered_papers
            if paper.get("year") == selected_year
        ]

    # Open Access filter
    if access_filter == "Open Access":

        filtered_papers = [
            paper
            for paper in filtered_papers
            if paper.get("open_access", False)
        ]

    elif access_filter == "Not Open Access":

        filtered_papers = [
            paper
            for paper in filtered_papers
            if not paper.get("open_access", False)
        ]

    # ========================================================
    # RESULTS COUNT
    # ========================================================

    st.markdown("")

    st.write(
        f"Showing **{len(filtered_papers)}** "
        f"of **{total_papers}** papers"
    )

    # ========================================================
    # PAPER CARDS
    # ========================================================

    if not filtered_papers:

        st.info(
            "No papers match your current search and filters."
        )

        return

    for paper in filtered_papers:

        st.markdown(
            """
            <div style="
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 14px;
                padding: 22px;
                margin-bottom: 16px;
                box-shadow: 0 2px 8px rgba(15,23,42,0.04);
            ">
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div style="
                font-size: 19px;
                font-weight: 750;
                color: #0F172A;
                margin-bottom: 8px;
            ">
                {paper.get("title", "Untitled Paper")}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # AUTHORS
        # ----------------------------------------------------

        authors = ", ".join(
            paper.get("authors", [])
        )

        st.markdown(
            f"""
            <div style="
                font-size: 13px;
                color: #64748B;
                margin-bottom: 15px;
            ">
                👥 {authors}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # PAPER INFORMATION
        # ----------------------------------------------------

        info1, info2, info3, info4 = st.columns(4)

        with info1:

            st.markdown(
                f"""
                <div style="
                    font-size: 11px;
                    color: #94A3B8;
                ">
                    YEAR
                </div>

                <div style="
                    font-size: 14px;
                    font-weight: 650;
                    color: #334155;
                    margin-top: 3px;
                ">
                    {paper.get("year", "N/A")}
                </div>
                """,
                unsafe_allow_html=True
            )

        with info2:

            st.markdown(
                f"""
                <div style="
                    font-size: 11px;
                    color: #94A3B8;
                ">
                    CITATIONS
                </div>

                <div style="
                    font-size: 14px;
                    font-weight: 650;
                    color: #334155;
                    margin-top: 3px;
                ">
                    {paper.get("citations", 0):,}
                </div>
                """,
                unsafe_allow_html=True
            )

        with info3:

            access_status = (
                "🟢 Open Access"
                if paper.get("open_access", False)
                else "🔴 Restricted"
            )

            st.markdown(
                f"""
                <div style="
                    font-size: 11px;
                    color: #94A3B8;
                ">
                    ACCESS
                </div>

                <div style="
                    font-size: 14px;
                    font-weight: 650;
                    color: #334155;
                    margin-top: 3px;
                ">
                    {access_status}
                </div>
                """,
                unsafe_allow_html=True
            )

        with info4:

            pdf_status = (
                "🟢 Available"
                if paper.get("pdf_available", False)
                else "⚪ Not Available"
            )

            st.markdown(
                f"""
                <div style="
                    font-size: 11px;
                    color: #94A3B8;
                ">
                    PDF
                </div>

                <div style="
                    font-size: 14px;
                    font-weight: 650;
                    color: #334155;
                    margin-top: 3px;
                ">
                    {pdf_status}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # DOI
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div style="
                background-color: #F8FAFC;
                border-radius: 8px;
                padding: 9px 12px;
                margin-top: 16px;
                font-size: 12px;
                color: #475569;
            ">
                <strong>DOI:</strong> {paper.get("doi", "N/A")}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")