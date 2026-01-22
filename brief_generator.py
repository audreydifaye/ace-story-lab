import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# DEBUG: VERSION CHECK
# ---------------------------------------------------------
# This will show us EXACTLY what version is running on the server.
st.sidebar.write(f"Library Version: {genai.__version__}")

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.text_input("Enter API Key", type="password")

if not api_key:
    st.stop()

genai.configure(api_key=api_key)

# Use the standard Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------------------------------------------------------
# APP UI
# ---------------------------------------------------------
st.set_page_config(page_title="ACE Story Lab", page_icon="🎬", layout="centered")
st.title("🎬 ACE Director's Brief")

col1, col2 = st.columns(2)
with col1:
    url = st.text_input("Target URL", "https://www.mdartplasticsurgery.com/")
with col2:
    industry = st.text_input("Industry", "Gender Affirming Surgery")

if st.button("Generate Treatment"):
    with st.spinner("🕵️‍♂️  Searching the live web..."):
        try:
            prompt = f"""
            Act as a Hollywood Documentary Researcher.
            I am making a film for: {url} in the {industry} space.
            
            Step 1: SEARCH the web for recent news, technology, and competitors.
            Step 2: Create a Director's Brief with:
            - Logline
            - The Villain (Specific Conflict)
            - Signature Visuals (Drone, Macro, Human)
            - Competitors & The Gap
            """
            
            # -----------------------------------------------------
            # THE FIX: SIMPLE STRING
            # This works on version 0.8.3+
            # If this errors, the server is definitely on an old version.
            # -----------------------------------------------------
            response = model.generate_content(
                prompt,
                tools='google_search' 
            )
            
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("If you see 'only code_execution is allowed', go to Manage App -> Reboot.")
