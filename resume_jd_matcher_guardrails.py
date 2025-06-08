import streamlit as st
from openai import OpenAI
import datetime

# Set up page
st.set_page_config(page_title="Resume–JD Matcher AI", layout="centered")
st.title("🤖 Resume–JD Matcher with AI")
st.write("Upload your resume and job description. Get a tailored match summary.")

# App configuration
MODE = st.secrets.get("MODE", "demo")  # 'demo' or 'paid'
MAX_FREE_REQUESTS = 5

# Session-based usage tracking
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# User input
resume_text = st.text_area("📄 Paste your Resume text here:", height=200)
jd_text = st.text_area("🧾 Paste the Job Description here:", height=200)

# Warning if free tier is about to expire
if MODE == "demo" and st.session_state.usage_count >= MAX_FREE_REQUESTS:
    st.error("⚠️ You've reached the limit of free summaries.")
    st.markdown("👉 [Click here to upgrade](https://buy.stripe.com/) to continue using GPT-4o.")
else:
    if st.button("🚀 Generate Match Summary"):
        if resume_text.strip() and jd_text.strip():
            with st.spinner("Analyzing with GPT..."):
                prompt = f"""Given the resume below:

{resume_text}

And the job description below:

{jd_text}

Generate a short summary evaluating how well the resume matches the JD.
Highlight:
- Strengths of the candidate
- Gaps or missing requirements
- Suggestions to improve resume alignment"""

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o" if MODE == "paid" else "gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content
                    st.subheader("🔍 Match Summary")
                    st.write(result)

                    # Increment usage only in demo mode
                    if MODE == "demo":
                        st.session_state.usage_count += 1

                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
        else:
            st.warning("Please paste both resume and job description.")

# Show upgrade section in demo mode
if MODE == "demo":
    st.markdown("---")
    st.info("🔓 Want unlimited access with GPT-4o?")
    st.markdown("Upgrade to premium for ₹199/month [🔗 Pay Now](https://buy.stripe.com/)")