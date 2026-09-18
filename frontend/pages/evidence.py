import streamlit as st


def render_evidence_page(data):
    """
    Displays research claims and their supporting evidence.
    Uses mock data until the backend evidence-verification
    pipeline is connected.
    """

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🔎 Evidence Analysis")

    st.markdown(
        "Review research claims and trace them back to "
        "supporting papers and evidence chunks."
    )

    st.divider()

    # ========================================================
    # EVIDENCE DATA
    # ========================================================

    evidence = data.get("evidence", [])

    if not evidence:
        st.warning("No evidence records available.")
        return

    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    total_claims = len(evidence)

    supported_claims = sum(
        1
        for item in evidence
        if item.get("verification_status") == "Supported"
    )

    average_confidence = (
        sum(
            item.get("confidence", 0)
            for item in evidence
        )
        / total_claims
        if total_claims
        else 0
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "🔎 Claims",
            total_claims
        )

    with metric2:
        st.metric(
            "✅ Supported",
            supported_claims
        )

    with metric3:
        st.metric(
            "🎯 Avg. Confidence",
            f"{average_confidence:.0%}"
        )

    st.markdown("")

    # ========================================================
    # SEARCH
    # ========================================================

    search_query = st.text_input(
        "Search Evidence",
        placeholder="Search claims, papers or evidence text..."
    )

    # ========================================================
    # FILTER EVIDENCE
    # ========================================================

    filtered_evidence = evidence.copy()

    if search_query:

        query = search_query.lower().strip()

        filtered_evidence = [
            item
            for item in filtered_evidence
            if (
                query in item.get("claim", "").lower()
                or query in item.get("paper_title", "").lower()
                or query in item.get("evidence_text", "").lower()
            )
        ]

    st.markdown(
        f"Showing **{len(filtered_evidence)}** "
        f"of **{total_claims}** evidence records"
    )

    # ========================================================
    # EVIDENCE CARDS
    # ========================================================

    for index, item in enumerate(filtered_evidence):

        claim = item.get(
            "claim",
            "No claim available."
        )

        confidence = item.get(
            "confidence",
            0
        )

        paper_title = item.get(
            "paper_title",
            "Unknown Paper"
        )

        paper_year = item.get(
            "paper_year",
            "N/A"
        )

        section = item.get(
            "section",
            "N/A"
        )

        chunk = item.get(
            "chunk",
            "N/A"
        )

        evidence_text = item.get(
            "evidence_text",
            "No evidence text available."
        )

        verification_status = item.get(
            "verification_status",
            "Unknown"
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if verification_status == "Supported":

            status_html = """
                <span style="
                    background-color:#DCFCE7;
                    color:#166534;
                    padding:5px 10px;
                    border-radius:20px;
                    font-size:11px;
                    font-weight:700;
                ">
                    ✓ SUPPORTED
                </span>
            """

        elif verification_status == "Partially Supported":

            status_html = """
                <span style="
                    background-color:#FEF3C7;
                    color:#92400E;
                    padding:5px 10px;
                    border-radius:20px;
                    font-size:11px;
                    font-weight:700;
                ">
                    ⚠ PARTIALLY SUPPORTED
                </span>
            """

        else:

            status_html = """
                <span style="
                    background-color:#FEE2E2;
                    color:#991B1B;
                    padding:5px 10px;
                    border-radius:20px;
                    font-size:11px;
                    font-weight:700;
                ">
                    ? UNVERIFIED
                </span>
            """

        # ----------------------------------------------------
        # CARD
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div style="
                background-color:white;
                border:1px solid #E2E8F0;
                border-radius:15px;
                padding:22px;
                margin-top:18px;
                box-shadow:0 2px 8px rgba(15,23,42,0.04);
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:12px;
                ">

                    <div style="
                        font-size:11px;
                        color:#94A3B8;
                        font-weight:700;
                        letter-spacing:0.7px;
                    ">
                        CLAIM {index + 1}
                    </div>

                    {status_html}

                </div>

                <div style="
                    font-size:17px;
                    font-weight:750;
                    color:#0F172A;
                    line-height:1.5;
                    margin-bottom:18px;
                ">
                    {claim}
                </div>

                <div style="
                    background-color:#F8FAFC;
                    border-radius:10px;
                    padding:15px;
                    margin-bottom:15px;
                ">

                    <div style="
                        font-size:10px;
                        color:#94A3B8;
                        font-weight:700;
                        letter-spacing:0.6px;
                    ">
                        SUPPORTING EVIDENCE
                    </div>

                    <div style="
                        font-size:14px;
                        color:#475569;
                        line-height:1.6;
                        margin-top:7px;
                    ">
                        “{evidence_text}”
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # DETAILS
        # ----------------------------------------------------

        detail1, detail2, detail3, detail4 = st.columns(4)

        with detail1:

            st.markdown(
                f"""
                **Supporting Paper**

                {paper_title}
                """,
            )

        with detail2:

            st.markdown(
                f"""
                **Year**

                {paper_year}
                """,
            )

        with detail3:

            st.markdown(
                f"""
                **Location**

                {section}
                """,
            )

        with detail4:

            st.markdown(
                f"""
                **Reference**

                {chunk}
                """,
            )

        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        st.markdown("")

        st.write(
            f"**Evidence Confidence: {confidence:.0%}**"
        )

        st.progress(
            min(max(confidence, 0), 1)
        )

        st.divider()