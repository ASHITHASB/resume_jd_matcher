import streamlit as st
from openai import OpenAI

# Streamlit page setup
st.set_page_config(page_title="Resume–JD Matcher AI", layout="centered")

st.title("🤖 Resume–JD Matcher with AI")
st.write("Upload your resume and job description. Get a tailored match summary.")

# Load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Input fields
resume_text = st.text_area("📄 Paste your Resume text here:", height=200)
jd_text = st.text_area("🧾 Paste the Job Description here:", height=200)

# Generate response
if st.button("🚀 Generate Match Summary"):
    if resume_text.strip() and jd_text.strip():
        with st.spinner("Analyzing with GPT-4o..."):
            prompt = f"""
Given the resume below:

{resume_text}

And the job description below:

{jd_text}

Generate a short summary evaluating how well the resume matches the JD.
Highlight:
- Strengths of the candidate
- Gaps or missing requirements
- Suggestions to improve resume alignment
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader("🔍 Match Summary")
            st.write(response.choices[0].message.content)
    else:
        st.warning("Please paste both resume and job description.")
