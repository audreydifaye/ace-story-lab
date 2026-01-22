import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS  # <--- The new Search Engine

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
model = genai.GenerativeModel('gemini-2.5-flash')

# ---------------------------------------------------------
# HELPER: THE SEARCH FUNCTION
# ---------------------------------------------------------
def get_intel(query):
    """Searches the web and returns a clean text summary."""
    try:
        # Limit to 5 results to keep it fast and relevant
        results = DDGS().text(query, max_results=5)
        intel = ""
        for r in results:
            intel += f"- SOURCE: {r['title']}\n  CONTENT: {r['body']}\n\n"
        return intel
    except Exception as e:
        return f"Search Error: {e}"

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
            # 1. SEARCH MANUALLY
            # We fetch the data first, then feed it to the AI.
            search_query = f"{url} {industry} competitors news mission"
            raw_intel = get_intel(search_query)
            
            # 2. THE PROMPT (Now includes the intel directly)
            prompt = f"""
            Act as a Hollywood Documentary Researcher for ACE Story Lab.
            I am making a brand film for: {url} in the {industry} space.
            
            HERE IS THE LIVE INTEL I FOUND:
            {raw_intel}
            
            MISSION: Use the intel above to find the "Cinematic Truth" behind this company.
            Generate the "Director's Brief":
            
            ## 🎥 PART 1: THE NARRATIVE ARC
            * **The Logline:** (1 sentence summary)
            * **The Conflict:** (What SPECIFIC problem are they fighting? Use analogies.)
            * **The Stakes:** (What happens if the conflict doesn't get resolved?)
            
            ## 🔭 PART 2: VISUAL CONCEPTS
            * **Signature Shots:** (3 distinct visual concepts for the director to consider.)

            ## 🕵️‍♂️ PART 3: COMPETITOR INTEL
            * **The Competitors:** (Identify competitors from the intel or your knowledge).
            * **The Gap:** (How do we beat their marketing?)
            """
            
            # 3. GENERATE
            # No 'tools' parameter needed anymore! pure text.
            response = model.generate_content(prompt)
            
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")

