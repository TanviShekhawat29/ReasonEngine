import streamlit as st


# =====================================================
# MESSAGE HELPERS
# =====================================================

def success(message: str):
    """
    Display a success message.
    """
    st.success(message)


def error(message: str):
    """
    Display an error message.
    """
    st.error(message)


def info(message: str):
    """
    Display an informational message.
    """
    st.info(message)


# =====================================================
# CONFIDENCE LABEL
# =====================================================

def confidence_label(score: int) -> str:
    """
    Convert confidence score into a readable label.
    """

    if score >= 90:
        return "Excellent Confidence"

    if score >= 80:
        return "Very High Confidence"

    if score >= 70:
        return "High Confidence"

    if score >= 60:
        return "Good Confidence"

    if score >= 50:
        return "Moderate Confidence"

    if score >= 35:
        return "Low Confidence"

    return "Very Low Confidence"


# =====================================================
# PAGE SECTION TITLE
# =====================================================

def section(title: str):
    """
    Render a section title with consistent spacing.
    """
    st.markdown(f"## {title}")


# =====================================================
# DIVIDER
# =====================================================

def divider():
    st.markdown("---")