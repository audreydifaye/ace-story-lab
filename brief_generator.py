import streamlit as st
import google.generativeai as genai
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # ⚠️ REPLACE WITH YOUR NEW KEY FOR LOCAL TESTING
    api_key = "AIzaSy..." 

genai.configure(api_key=api_key)

# FIX 1: Use the correct model name (1.5, not 2.5)
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------------------------------------------------------
# APP UI
# ---------------------------------------------------------
st.set_page_config(page_title="ACE Story Lab", page_icon="🎬", layout="centered")

st.title("🎬 ACE Director's Brief")
st.markdown("*The 'Intelligence Layer' for Documentary Production*")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    url = st.text_input("Target URL", "https://www.mdartplasticsurgery.com/")
with col2:
    industry = st.text_input("Industry", "Gender Affirming Surgery")

# ---------------------------------------------------------
# THE LOGIC
# ---------------------------------------------------------
# ... (Keep your imports and UI setup at the top) ...

if st.button("Generate Treatment"):
    with st.spinner("🕵️‍♂️  Searching the live web & Designing the film..."):
        try:
            # 1. DEFINE THE TOOL MANUALLY (The Fix)
            # This constructs the "Google Search" tool using the low-level library
            # so we don't trigger the "String Error".
            search_tool = genai.protos.Tool(
                google_search_retrieval=genai.protos.GoogleSearchRetrieval(
                    dynamic_retrieval_config=genai.protos.DynamicRetrievalConfig(
                        mode=genai.protos.DynamicRetrievalConfig.Mode.MODE_DYNAMIC
                    )
                )
            )

            # 2. THE PROMPT
            prompt = f"""
            Act as a Hollywood Documentary Researcher for ACE Story Lab.
            I am producing a high-end "Brand Documentary" for: {url} in the {industry} space.
            
            MISSION: Find the "Cinematic Truth" behind this company.
            
            Step 1: SEARCH the web for this company's recent news, technology, and competitors.
            Step 2: Generate the "Director's Brief":
            
            ## 🎥 PART 1: THE NARRATIVE ARC
            * **The Logline:** (1 sentence summary)
            * **The Conflict:** (What SPECIFIC problem are they fighting? Use analogies.)
            * **The Protagonist:** (The Customer/Solution. How do they triumph?)
            * **The Stakes:** (What happens if the Villain wins?)
            
            ## 🔭 PART 2: VISUAL CONCEPTS
            * **Signature Shots:** (3 distinct visual concepts: macro, drone, human.)

            ## ⚡ PART 3: THE HOOK
            * **The 15s Scroll-Stopper:** (Visual punch for LinkedIn/Ads.)
            
            ## 🕵️‍♂️ PART 4: COMPETITOR INTEL
            * **The Competitors:** (List 3 major competitors found in search).
            * **The Gap:** (How do we beat their marketing?)
            """
            # 3. GENERATE (Pass the tool object, NOT a string)
            response = model.generate_content(
                prompt,
                tools=[{'google_search': {}}] 
            )
            
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
