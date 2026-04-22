import streamlit as st
import os
import chromadb
from google import genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(page_title="Endee AI", page_icon="🚀", layout="wide")
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
    client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    db_client = chromadb.PersistentClient(path="./codebase_db")
    collection = db_client.get_or_create_collection(name="project_knowledge")
    return client_ai, embed_model, collection

client_ai, embed_model, collection = init_resources()

# --- 2. SIDEBAR UTILITIES ---
with st.sidebar:
    st.title("⚙️ System Control")
    st.info(f"Knowledge Base: {collection.count()} snippets")
    
    if st.button("🔄 Re-index Codebase"):
        with st.spinner("Scanning files..."):
            # Put your index_codebase logic call here if needed
            st.success("Codebase refreshed!")
            st.rerun()
            
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 3. CHAT INTERFACE ---
st.title("🚀 Endee: AI Codebase Assistant")
st.caption("Analyzing HNSW implementation and project logic in real-time.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about HNSW, app logic, or C++ internals..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying Vector DB & Gemini..."):
            # RAG Step 1: Retrieval
            q_vec = embed_model.encode(prompt).tolist()
            res = collection.query(query_embeddings=[q_vec], n_results=4)
            
            if not res['documents'][0]:
                ans = "I couldn't find any relevant code for that query."
            else:
                # RAG Step 2: Generation
                context = "\n\n".join(res['documents'][0])
                try:
                    # Using the frontier Gemini 3 model
                    response = client_ai.models.generate_content(
                        model='gemini-3-flash-preview',
                        contents=f"Context:\n{context}\n\nQuestion: {prompt}. Explain based on the code."
                    )
                    ans = response.text
                except Exception as e:
                    ans = f"⚠️ AI Error: {e}"

            st.markdown(ans)
            with st.expander("📍 Referenced Files"):
                for path in set(res['metadatas'][0][i]['path'] for i in range(len(res['metadatas'][0]))):
                    st.code(path)
            
            st.session_state.messages.append({"role": "assistant", "content": ans})