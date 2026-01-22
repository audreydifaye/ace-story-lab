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
            * **The Conflict:** (What SPECIFIC problem are they fighting? Provide 2-3 options for how to position the issue creatively, empathetically and with brevity, and gravitas. Include analogies if appropriate.)
            * **The Protagonist:** (Not the company, but the *Solution/Customer*. How do they triumph?)
            * **The Stakes:** (What happens if the Villain wins? Make it emotional.)
            
            ## 🔭 PART 2: VISUAL CONCEPTS ("The Signature Shots")
            * **Three distinct visual concepts:** (Based on what we've found out about the target audience, develop a fresh visual concept that will highlight and set their business as an outstanding leader in their industry. Consider macro, drone, human shots, product shots, or others if more compelling)

            ## ⚡ PART 3: The Narrative Hook (Phase 2)
            * **The 15s Scroll-Stopper:** (A fast-paced hook idea for LinkedIn, Meta, TikTok, YT, or other ads. What is the visual punch? Why would we focus on a platform vs others?)
            
            ## 🕵️‍♂️ PART 4: COMPETITOR INTEL (Live Search)
            * **The Competitors:** (List 3 major competitors found in search).
            * **The Gap:** (What is their current boring marketing angle, and how do we beat it with Cinema?)
            """
            
            # 2. GENERATE WITH GOOGLE SEARCH (GROUNDING)
            # This 'tools' parameter connects it to the live internet
            response = model.generate_content(
                prompt,
                tools='code_execution'
            )
            
            # 3. DISPLAY OUTPUT
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Tip: If you get a 404 on tools, make sure you are using 'gemini-1.5-flash' or 'gemini-1.5-pro'.")





