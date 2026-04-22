import os
import chromadb
from google import genai  # Official new SDK
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 1. LOAD CONFIGURATION
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    exit()

# Initialize the NEW Gemini 2.0 Client
client_ai = genai.Client(api_key=GEMINI_API_KEY)

# Setup AI Memory (Embeddings + Vector DB)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "codebase_db")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
client_db = chromadb.PersistentClient(path=DB_PATH)
collection = client_db.get_or_create_collection(name="project_knowledge")

SUPPORTED_EXTENSIONS = {'.java', '.py', '.js', '.sql', '.cpp', '.h', '.html', '.css'}

def index_codebase(root_path):
    print(f"\n--- Scanning Codebase: {root_path} ---")
    count = 0
    for root, dirs, files in os.walk(root_path):
        # Skip heavy/unnecessary folders
        dirs[:] = [d for d in dirs if d not in ['codebase_db', '.venv', '.git', '__pycache__', 'third_party']]
        
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if not content.strip(): continue
                        
                        # Chunking: AI models handle ~2000 chars best
                        chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
                        for idx, chunk in enumerate(chunks):
                            vector = embed_model.encode(chunk).tolist()
                            rel_path = os.path.relpath(file_path, root_path)
                            collection.add(
                                embeddings=[vector],
                                documents=[chunk],
                                metadatas=[{"path": rel_path}],
                                ids=[f"{rel_path}_{idx}_{count}"]
                            )
                        count += 1
                        print(f"✅ Indexed: {rel_path}")
                except Exception as e:
                    print(f"⚠️ Skip {file}: {e}")
    print(f"--- Indexing Complete! {count} files processed. ---")

def ask_ai(query):
    """
    Performs RAG: Retrieves code snippets then asks Gemini to explain them.
    """
    # A. RETRIEVE
    query_vector = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_vector], n_results=4)
    
    if not results['documents'][0]:
        print("I couldn't find any relevant code snippets.")
        return

    # B. CONSTRUCT CONTEXT
    context_text = ""
    sources = set()
    for i in range(len(results['documents'][0])):
        path = results['metadatas'][0][i]['path']
        code = results['documents'][0][i]
        context_text += f"\nFILE: {path}\nCODE:\n{code}\n{'-'*20}"
        sources.add(path)

    # C. GENERATE RESPONSE
    print("\n🤖 Thinking...")
    try:
        # Using Gemini 2.0 Flash for maximum speed and intelligence
        response = client_ai.models.generate_content(
            model='gemini-3-flash-preview',
            contents=f"""
            You are an expert Software Architect. Answer the user's question based ONLY on the code snippets provided.
            
            CODE CONTEXT:
            {context_text}
            
            USER QUESTION: {query}
            
            Explain clearly which files contain the logic and how it works.
            """
        )
        
        print("\n" + "✨ AI EXPLANATION " + "="*40)
        print(response.text)
        print("="*60)
        print(f"📍 Sources analyzed: {', '.join(sources)}")
        
    except Exception as e:
        print(f"❌ AI Error: {e}")

if __name__ == "__main__":
    # Index if the DB is empty
    if collection.count() == 0:
        index_codebase(BASE_DIR)
    else:
        print(f"✅ Database loaded with {collection.count()} code snippets.")

    print("\n🚀 CODEBASE ASSISTANT ONLINE")
    print("Type your questions about the code or 'exit' to quit.")
    
    while True:
        user_input = input("\n🤔 What would you like to know? > ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        if not user_input.strip():
            continue
        ask_ai(user_input)