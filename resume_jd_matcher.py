import streamlit as st
import openai

st.set_page_config(page_title="Resume–JD Matcher AI", layout="centered")

st.title("🤖 Resume–JD Matcher with AI")
st.write("Upload your resume and job description. Get a tailored match summary.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

resume_text = st.text_area("Paste your Resume text here:", height=200)
jd_text = st.text_area("Paste the Job Description here:", height=200)

if st.button("Generate Match Summary"):
    if resume_text and jd_text:
        with st.spinner("Analyzing with GPT..."):
            prompt = f"Given the resume below:

{resume_text}

And the job description below:

{jd_text}

Generate a short summary evaluating how well the resume matches the JD, strengths, gaps, and suggestions for improvement."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader("🔍 Match Summary")
            st.write(response.choices[0].message["content"])
    else:
        st.warning("Please paste both resume and job description.")