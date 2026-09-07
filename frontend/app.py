import streamlit as st

from api.client import api
from utils.helpers import (
    success,
    error,
    info,
    confidence_label,
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Reason Engine",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# SESSION STATE
# =====================================================

DEFAULT_STATE = {
    "uploaded": False,
    "upload_result": None,
    "summary": None,
    "questions": None,
    "answer": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown(
    """
<style>

html,
body,
[class*="css"]{
    font-family:Inter,sans-serif;
}

.block-container{
    max-width:1250px;
    padding-top:2rem;
    padding-bottom:2rem;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.hero{
    padding:35px;
    border-radius:24px;
    background:linear-gradient(135deg,#2563EB,#1E40AF);
    color:white;
    margin-bottom:25px;
}

.hero h1{
    font-size:46px;
    margin-bottom:8px;
}

.hero p{
    font-size:18px;
    opacity:.92;
}

.card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:24px;
    margin-bottom:20px;
    box-shadow:0 8px 24px rgba(0,0,0,.05);
}

.metric-card{
    background:#F8FAFC;
    border-radius:16px;
    border:1px solid #E5E7EB;
    padding:20px;
    text-align:center;
}

.topic{
    display:inline-block;
    padding:8px 14px;
    border-radius:999px;
    background:#EFF6FF;
    color:#2563EB;
    font-weight:600;
    margin:5px;
}

.question{
    background:#F9FAFB;
    border-left:5px solid #2563EB;
    padding:14px;
    border-radius:10px;
    margin-bottom:10px;
}

.answer{
    background:#FFFFFF;
    border-radius:18px;
    border:1px solid #E5E7EB;
    padding:25px;
    line-height:1.8;
}

.footer{
    color:#9CA3AF;
    text-align:center;
    padding:40px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("Reason Engine")

    st.caption("AI Document Intelligence")

    st.divider()

    try:

        health = api.health()

        st.success("Backend Connected")

        st.write(f"Status : **{health['status']}**")
        st.write(f"Application : **{health['application']}**")

    except Exception:

        st.error("Backend Offline")

    st.divider()

    st.markdown(
        """
### Workflow

✔ Upload PDF

✔ Generate Embeddings

✔ Store in Qdrant

✔ AI Summary

✔ Suggested Questions

✔ Semantic Search

✔ AI Question Answering
"""
    )

    st.divider()

    st.caption("Summer Internship Project")

# =====================================================
# HERO
# =====================================================

st.markdown(
    """
<div class="hero">

<h1>Reason Engine</h1>

<p>
AI-powered Document Question Answering using
FastAPI, Qdrant, Sentence Transformers and Groq.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# DOCUMENT UPLOAD
# =====================================================

st.header("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

if st.button(
    "Upload & Process",
    use_container_width=True,
):

    if uploaded_file is None:

        error("Please choose a PDF document.")

    else:

        with st.spinner("Processing document..."):

            try:

                result = api.upload_pdf(uploaded_file)

                summary = api.get_summary()

                questions = api.get_questions()

                st.session_state.uploaded = True
                st.session_state.upload_result = result
                st.session_state.summary = summary
                st.session_state.questions = questions

                success("Document processed successfully.")

            except Exception as e:

                error(str(e))
# =====================================================
# DOCUMENT OVERVIEW
# =====================================================

if st.session_state.uploaded:

    st.divider()

    st.header("📊 Document Overview")

    upload = st.session_state.upload_result

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Pages",
            upload["pages"],
        )

    with c2:
        st.metric(
            "Chunks",
            upload["chunks"],
        )

    with c3:
        st.metric(
            "Vectors",
            upload["vectors"],
        )

    st.write("")

# =====================================================
# AI SUMMARY
# =====================================================

if st.session_state.summary is not None:

    summary = st.session_state.summary

    st.subheader("📝 AI Generated Summary")

    st.markdown(
        f"""
<div class="card">

{summary["summary"]}

</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================
# TOPICS
# =====================================================

    if summary.get("topics"):

        st.subheader("🏷 Key Topics")

        topic_html = ""

        for topic in summary["topics"]:

            topic_html += f"""
<span class="topic">{topic}</span>
"""

        st.markdown(
            topic_html,
            unsafe_allow_html=True,
        )

# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

if st.session_state.questions is not None:

    st.write("")
    st.subheader("💡 Suggested Questions")

    for question in st.session_state.questions["questions"]:

        st.markdown(
            f"""
<div class="question">

{question}

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

# =====================================================
# QUESTION ANSWERING
# =====================================================

if st.session_state.uploaded:

    st.header("🤖 Ask Questions")

    question = st.text_area(
        "Ask anything about the uploaded document",
        placeholder="Example: What are IBM's strategic priorities?",
        height=140,
    )

    ask = st.button(
        "Ask AI",
        use_container_width=True,
    )

    if ask:

        if not question.strip():

            error("Please enter a question.")

        else:

            with st.spinner(
                "Searching document and generating answer..."
            ):

                try:

                    response = api.ask_question(question)

                    st.session_state.answer = response

                except Exception as e:

                    error(str(e))
# =====================================================
# DISPLAY AI ANSWER
# =====================================================

if st.session_state.answer is not None:

    response = st.session_state.answer

    st.divider()

    st.subheader("💬 AI Answer")

    st.markdown(
        f"""
<div class="answer">

{response["answer"]}

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

# =====================================================
# CONFIDENCE
# =====================================================

    confidence = response["confidence"]

    st.subheader("📈 Confidence Score")

    st.progress(confidence / 100)

    left, right = st.columns([1, 3])

    with left:

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

    with right:

        st.info(
            f"""
**{confidence_label(confidence)}**

{response["reason"]}
"""
        )

# =====================================================
# SOURCE CHUNKS
# =====================================================

    st.write("")
    st.subheader("📚 Retrieved Source Chunks")

    sources = response["sources"]

    if len(sources) == 0:

        info("No source chunks returned.")

    else:

        for i, source in enumerate(sources, start=1):

            with st.expander(
                f"Chunk {i} • Similarity {source['score']:.4f}"
            ):

                st.markdown(
                    f"**Source:** `{source['source']}`"
                )

                st.write(source["text"])

# =====================================================
# NEW DOCUMENT
# =====================================================

st.divider()

left, right = st.columns([1, 4])

with left:

    if st.button(
        "🔄 New Document",
        use_container_width=True,
    ):

        for key in [
            "uploaded",
            "upload_result",
            "summary",
            "questions",
            "answer",
        ]:

            if key in st.session_state:

                del st.session_state[key]

        st.rerun()

with right:

    st.caption(
        "Uploading another PDF replaces the current indexed document."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
<br><br>

---

<div class="footer">

<h4>Reason Engine</h4>

AI-Powered Document Question Answering

<br>

Built using

<b>FastAPI</b> •
<b>Streamlit</b> •
<b>Qdrant</b> •
<b>Sentence Transformers</b> •
<b>Groq LLM</b>

<br><br>

Summer Internship Project • 2026

</div>
""",
    unsafe_allow_html=True,
)