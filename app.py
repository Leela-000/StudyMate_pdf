import streamlit as st
from backend.pdf_utils import extract_text_from_pdf
from backend.qa_model import answer_question
from backend.translator import translate_text
from backend.db import save_chat, get_chat_history
import uuid
import re

# Streamlit page config
st.set_page_config(page_title="StudyMate", layout="centered")

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found. Proceeding without it.")

# Animated header
st.markdown("## 📄 <span class='title'>StudyMate: Where PDFs Talk Back 🌐</span>", unsafe_allow_html=True)
st.markdown("### 💬 Upload. Ask. Get Instant Answers in Your Own Language!")

# File uploader
pdf = st.file_uploader("📂 Upload your PDF", type="pdf", label_visibility="collapsed")
session_id = str(uuid.uuid4())
file_text = ""

# Clean text utility
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove excessive whitespace
    text = re.sub(r'\n+', '\n', text)  # Collapse multiple newlines
    return text.strip()

# Process PDF
if pdf:
    extracted = extract_text_from_pdf(pdf)
    file_text = clean_text(extracted)
    st.success(f"✅ Uploaded: {pdf.name}")
    st.info(f"ℹ️ Only the first ~3000 characters of text will be used for faster answering.")

# Language selector
lang = st.selectbox("🌍 Select your language:", ["English", "Hindi", "Telugu", "Tamil", "Kannada"])

# Question input
user_input = st.text_input("💬 Ask a question about the PDF")

# Answering
if st.button("🚀 Get Answer"):
    if file_text and user_input:
        with st.spinner("Thinking..."):
            # Limit text length for clarity
            context = file_text[:3000]

            # Get the answer from QA model
            answer = answer_question(user_input, context)

            # Translate if needed
            if lang == "English":
                translated_answer = answer
            else:
                translated_answer = translate_text(answer, target_lang=lang)

            # Save chat history
            save_chat(session_id, user_input, translated_answer)

            # Info if answer is very short
            if len(translated_answer.split()) < 5:
                st.info("ℹ️ This answer is very short. Try rephrasing the question or uploading a more content-rich PDF.")

            # Display chat bubbles
            st.markdown(f"<div class='user-bubble'>🧑 {user_input}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bot-bubble'>🤖 {translated_answer}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a PDF and enter your question.")

# Chat history
st.markdown("---")
st.markdown("## 🕘 Previous Questions")
chat_history = get_chat_history(session_id)

for q, a in chat_history:
    st.markdown(f"<div class='user-bubble'>🧑 {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'>🤖 {a}</div>", unsafe_allow_html=True)
