import streamlit as st
import google.generativeai as genai

# OLD (Don't use this for cloud):
# API_KEY = "AIzaSy..."

# NEW (Cloud-Ready):
import os
# Try to get the key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("No API Key found in Secrets!")
    st.stop()

genai.configure(api_key=api_key)

st.title("🎥 ACE Story Lab: Director's Brief")

# Input fields for company URL and industry
company_url = st.text_input("Company URL")
industry = st.text_input("Industry")

if st.button("Generate Brief"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not company_url or not industry:
        st.error("Please fill in both the Company URL and Industry.")
    else:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        user_prompt = (
            "Act as a Hollywood Documentary Researcher. "
            f"I am making a brand film for: {company_url} in the {industry} space. "
            "Please browse your internal knowledge about this sector and generate:\n\n"
            "The Logline: (1 sentence summary)\n\n"
            "The Villain: (What problem are they fighting?)\n\n"
            "Visual Concepts: (3 specific ideas for cinematic shots)\n\n"
            'The "Why": (Why does this company matter?)'
        )

        try:
            response = model.generate_content(user_prompt)
            output = response.text if hasattr(response, "text") else str(response)
            st.markdown(output)
        except Exception as e:
            st.error(f"Error: {e}")