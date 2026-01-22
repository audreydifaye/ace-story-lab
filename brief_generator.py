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

# ⚠️ FIX: Changed '2.5' back to '1.5' to prevent 404 errors
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

# ---------------------------------------------------------
# THE LOGIC
# ---------------------------------------------------------
if st.button("Generate Treatment"):
    with st.spinner("🕵️‍♂️  Searching the live web..."):
        try:
            # 1. THE "PROTO" BYPASS
            # We build the object manually to force the library to accept the tool.
            tool = genai.protos.Tool(
                google_search=genai.protos.GoogleSearch()
            )

            # 2. THE PROMPT
            prompt = f"""
            Act as a Hollywood Documentary Researcher for ACE Story Lab.
            I am making a brand film for: {url} in the {industry} space.
            
            MISSION: Find the "Cinematic Truth" behind this company.
            
            Step 1: SEARCH the web for this company's recent news, technology, and competitors.
            Step 2: Generate the "Director's Brief":
            
            ## 🎥 PART 1: THE NARRATIVE ARC
            * **The Logline:** (1 sentence summary)
            * **The Conflict:** (What SPECIFIC problem are they fighting? Use analogies.)
            * **The Stakes:** (What happens if the conflict doesn't get resolved?)
            
            ## 🔭 PART 2: VISUAL CONCEPTS
            * **Signature Shots:** (3 distinct visual concepts for the director to consider.)

            ## 🕵️‍♂️ PART 3: COMPETITOR INTEL
            * **The Competitors:** (List 3 major competitors found in search).
            * **The Gap:** (How do we beat their marketing?)
            """
            
            # 3. GENERATE
            # Pass the 'tool' object inside a list.
            response = model.generate_content(
                prompt,
                tools=[tool]
            )
            
            st
