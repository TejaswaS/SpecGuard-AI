import streamlit as st
import pandas as pd

from extraction.pdf_parser import extract_pdf_text
from extraction.llm_extractor import extract_product_information

from validation.rules import validate_product
from validation.scoring import calculate_quality_score

#   cd "C:\Users\TEJASWA SHARMA\OneDrive\Desktop\Projects\SpecGurad"
#   python -m streamlit run app.py


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="SpecGuard",
    page_icon="🛡️",
    layout="wide"
)


# -----------------------------------------
# HEADER
# -----------------------------------------

st.title("🛡️ SpecGuard")

st.subheader(
    "AI-Powered Industrial Product Specification Validator"
)

st.write(
    "Extract, validate and explain industrial product specifications "
    "from technical documents."
)


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.header("Document")

    uploaded_file = st.file_uploader(
        "Upload product datasheet",
        type=["pdf"]
    )

    st.divider()

    st.info(
        "SpecGuard extracts product specifications using AI "
        "and validates them using deterministic rules."
    )


# -----------------------------------------
# MAIN
# -----------------------------------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze Product",
        type="primary"
    ):

        try:

            # ----------------------------
            # STEP 1: PDF extraction
            # ----------------------------

            with st.spinner("Reading product document..."):

                file_bytes = uploaded_file.getvalue()

                pages = extract_pdf_text(
                    file_bytes
                )

            # ----------------------------
            # STEP 2: AI extraction
            # ----------------------------

            with st.spinner(
                "AI is extracting product specifications..."
            ):

                product = extract_product_information(
                    pages
                )

            # ----------------------------
            # STEP 3: Validation
            # ----------------------------

            with st.spinner(
                "Validating specifications..."
            ):

                issues = validate_product(
                    product
                )

                score = calculate_quality_score(
                    product,
                    issues
                )

            # Store results

            st.session_state.product = product
            st.session_state.issues = issues
            st.session_state.score = score

        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )


# -----------------------------------------
# DISPLAY RESULTS
# -----------------------------------------

if "product" in st.session_state:

    product = st.session_state.product
    issues = st.session_state.issues
    score = st.session_state.score

    st.divider()

    # -------------------------------------
    # PRODUCT HEADER
    # -------------------------------------

    st.header(
        f"📦 {product.product_name}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Quality Score",
            f"{score}/100"
        )

    with col2:
        st.metric(
            "Specifications",
            len(product.specifications)
        )

    with col3:

        errors = sum(
            1 for issue in issues
            if issue.severity == "ERROR"
        )

        st.metric(
            "Errors",
            errors
        )

    with col4:

        missing = sum(
            1 for issue in issues
            if issue.severity == "MISSING"
        )

        st.metric(
            "Missing",
            missing
        )

    # -------------------------------------
    # PRODUCT INFO
    # -------------------------------------

    st.subheader("Product Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.write(
            f"**Category:** "
            f"{product.category or 'Not specified'}"
        )

        st.write(
            f"**Manufacturer:** "
            f"{product.manufacturer or 'Not specified'}"
        )

    with info_col2:

        st.write(
            f"**Description:** "
            f"{product.description or 'Not specified'}"
        )

    # -------------------------------------
    # SPECIFICATIONS
    # -------------------------------------

    st.subheader("🔍 Extracted Specifications")

    data = []

    for spec in product.specifications:

        data.append({
            "Specification": spec.name,
            "Value": spec.value or "—",
            "Unit": spec.unit or "—",
            "Page": spec.page or "—"
        })

    if data:

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # -------------------------------------
    # VALIDATION
    # -------------------------------------

    st.subheader("⚠️ Validation Results")

    if not issues:

        st.success(
            "No validation issues detected."
        )

    else:

        for issue in issues:

            if issue.severity == "ERROR":

                st.error(
                    f"🔴 **{issue.field}** — "
                    f"{issue.message}"
                )

            elif issue.severity == "WARNING":

                st.warning(
                    f"🟡 **{issue.field}** — "
                    f"{issue.message}"
                )

            else:

                st.info(
                    f"🔵 **{issue.field}** — "
                    f"{issue.message}"
                )

            st.caption(
                f"Recommendation: {issue.recommendation}"
            )

    # -------------------------------------
    # EVIDENCE
    # -------------------------------------

    st.subheader("🔎 Source Evidence")

    for spec in product.specifications:

        with st.expander(
            f"{spec.name}: {spec.value or 'Not specified'}"
        ):

            st.write(
                f"**Page:** {spec.page or 'Unknown'}"
            )

            st.write(
                "**Evidence:**"
            )

            st.info(
                spec.source_text
                or "No source evidence available."
            )