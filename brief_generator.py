import streamlit as st
import google.generativeai as genai
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# Try to get key from Secrets (Cloud) or Hardcoded (Local)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # ⚠️ REPLACE WITH YOUR NEW KEY FOR LOCAL TESTING
    api_key = "AIzaSy..." 

genai.configure(api_key=api_key)

# We use the Flash model because it's fast and supports Search tools
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------------------------------------------------------
# APP UI
# ---------------------------------------------------------
st.set_page_config(page_title="ACE Story Lab", page_icon="🎬", layout="centered")

# Header
st.title("🎬 ACE Director's Brief")
st.markdown("*The 'Intelligence Layer' for Documentary Production*")
st.markdown("---")

# Inputs
col1, col2 = st.columns(2)
with col1:
    url = st.text_input("Target URL", "https://www.heirloomcarbon.com")
with col2:
    industry = st.text_input("Industry", "Climate Tech")

# ---------------------------------------------------------
# THE VIBE CODE LOGIC
# ---------------------------------------------------------
if st.button("Generate Treatment"):
    with st.spinner("🕵️‍♂️  Searching the live web & Designing the film..."):
        try:
            # 1. THE "ACE STORY LAB" PROMPT
            # This matches your Business Model (Phase 1: Hero Asset & Phase 2: Trailer Offensive)
            prompt = f"""
            Act as a Hollywood Documentary Researcher for ACE Story Lab.
            I am producing a high-end "Brand Documentary" (not a commercial) for: {url} in the {industry} space.
            
            MISSION: Find the "Cinematic Truth" behind this company. Do not write marketing copy. Write a film treatment.
            
            Step 1: SEARCH the web for this company's recent news, specific technology, and competitors.
            Step 2: Generate the following "Director's Brief":
            
            ## 🎥 PART 1: THE NARRATIVE ARC (Phase 1)
            * **The Logline:** (1 sentence summary of the film: "Interstellar meets National Geographic.")
            * **The Villain:** (What SPECIFIC problem are they fighting? e.g., "The Invisible Enemy of CO2" or "The Chaos of Data".)
            * **The Hero:** (Not the company, but the *Solution/Customer*. How do they triumph?)
            * **The Stakes:** (What happens if the Villain wins? Make it emotional.)
            
            ## 🔭 PART 2: VISUAL CONCEPTS ("The Signature Shots")
            * **The Macro Shot:** (A tactile, extreme close-up detail of their tech/product. e.g., "Crushing limestone" or "Pixels firing".)
            * **The Drone Shot:** (A sense of scale and gravity.)
            * **The Human Moment:** (A specific scene showing the people behind the machine.)

            ## ⚡ PART 3: THE TRAILER OFFENSIVE (Phase 2)
            * **The 15s Scroll-Stopper:** (A fast-paced hook idea for LinkedIn ads. What is the visual punch?)
            
            ## 🕵️‍♂️ PART 4: COMPETITOR INTEL (Live Search)
            * **The Competitors:** (List 3 major competitors found in search).
            * **The Gap:** (What is their current boring marketing angle, and how do we beat it with Cinema?)
            """
            
            # 2. GENERATE WITH GOOGLE SEARCH (GROUNDING)
            # This 'tools' parameter connects it to the live internet
            response = model.generate_content(
                prompt,
                tools='google_search_retrieval'
            )
            
            # 3. DISPLAY OUTPUT
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: If you get a 404 on tools, make sure you are using 'gemini-1.5-flash' or 'gemini-1.5-pro'.")


