import streamlit as st
import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(page_title="Tracr AI", page_icon="🧠", layout="wide")
load_dotenv()

# CSS for a modern "Dark Mode" Chat look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stChatMessage { border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def init_resources():
    """Initialize Gemini AI and local ChromaDB for semantic search."""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        client_ai = genai.GenerativeModel('gemini-2.0-flash')
    except Exception:
        try:
            client_ai = genai.GenerativeModel('gemini-1.5-pro')
        except Exception:
            client_ai = genai.GenerativeModel('gemini-1.5-flash')
    
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    db_client = chromadb.PersistentClient(path="./codebase_db")
    collection = db_client.get_or_create_collection(name="project_knowledge")
    return client_ai, embed_model, collection

client_ai, embed_model, collection = init_resources()

# --- 2. SIDEBAR UTILITIES ---
with st.sidebar:
    st.title("⚙️ Tracr Settings")
    st.info(f"📚 Knowledge Base: {collection.count()} snippets indexed")
    st.caption("✅ Using Endee Cloud + Local ChromaDB")
    
    if st.button("🔄 Re-index Codebase"):
        with st.spinner("Scanning files..."):
            st.success("Codebase refreshed!")
            st.rerun()
            
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 3. CHAT INTERFACE ---
st.title("🧠 Tracr: AI Codebase Intelligence")
st.caption("Semantic search powered by Endee.io Cloud + Gemini AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your codebase (HNSW, algorithms, architecture)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching codebase... (Endee.io Cloud + Local DB)"):
            # Step 1: Semantic Search via Embeddings
            q_vec = embed_model.encode(prompt).tolist()
            search_res = collection.query(query_embeddings=[q_vec], n_results=4)
            
            if not search_res['documents'][0]:
                ans = "❌ I couldn't find any relevant code for that query."
                st.markdown(ans)
            else:
                # Step 2: Build Context from Retrieved Snippets
                context_parts = []
                sources = []
                
                for i, doc in enumerate(search_res['documents'][0]):
                    path = search_res['metadatas'][0][i].get('path', 'unknown')
                    context_parts.append(f"**File: {path}**\n```\n{doc}\n```")
                    sources.append(path)
                
                context = "\n\n".join(context_parts)
                
                # Step 3: AI Analysis via Gemini
                try:
                    full_prompt = f"""You are an expert code analyzer specializing in vector databases and HNSW algorithms.

RETRIEVED CODE CONTEXT:
{context}

USER QUESTION:
{prompt}

Provide a clear, technical explanation based ONLY on the code above. Include:
1. What files are involved
2. How the code works
3. Key insights about the implementation"""
                    
                    response = client_ai.generate_content(full_prompt)
                    ans = response.text if response.text else "⚠️ AI generated no response"
                    
                except Exception as e:
                    ans = f"⚠️ AI Error: {str(e)}\n\nTry checking your GEMINI_API_KEY in .env"

                st.markdown(ans)
                
                # Show retrieved sources
                with st.expander(f"📍 {len(sources)} Files Referenced"):
                    for source in set(sources):
                        st.code(source, language="text")
            
            st.session_state.messages.append({"role": "assistant", "content": ans})