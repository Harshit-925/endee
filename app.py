import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from endee import Endee

# 1. LOAD CONFIGURATION
load_dotenv()
ENDEE_API_TOKEN = os.getenv("ENDEE_API_TOKEN")

# Setup AI Memory (Embeddings + Vector DB)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "codebase_db")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
client_db = chromadb.PersistentClient(path=DB_PATH)
collection = client_db.get_or_create_collection(name="project_knowledge")

# Setup Endee Cloud (optional, with fallback to ChromaDB)
client_endee = None
endee_index = None
USE_CLOUD = False

if ENDEE_API_TOKEN:
    try:
        client_endee = Endee(ENDEE_API_TOKEN)
        # Get or create 'codebaseindex'
        indexes = client_endee.list_indexes()
        if 'codebaseindex' in indexes:
            endee_index = client_endee.get_index('codebaseindex')
            USE_CLOUD = True
            print("☁️  Endee Cloud connected! Using cloud index 'codebaseindex'")
        else:
            print("⚠️  Cloud index 'codebaseindex' not found. Create it first, or using local ChromaDB only.")
    except Exception as e:
        print(f"⚠️  Endee Cloud unavailable ({e}). Falling back to local ChromaDB.")
else:
    print("ℹ️  ENDEE_API_TOKEN not set. Using local ChromaDB only.")

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
                            doc_id = f"{rel_path}_{idx}_{count}"
                            
                            # Index to LOCAL ChromaDB
                            collection.add(
                                embeddings=[vector],
                                documents=[chunk],
                                metadatas=[{"path": rel_path}],
                                ids=[doc_id]
                            )
                            
                            # Index to CLOUD if available
                            if USE_CLOUD and endee_index:
                                try:
                                    endee_index.add(
                                        vectors=[vector],
                                        documents=[chunk],
                                        metadatas=[{"path": rel_path}],
                                        ids=[doc_id]
                                    )
                                except Exception as e:
                                    print(f"  ⚠️  Cloud indexing skipped for {rel_path}: {e}")
                        
                        count += 1
                        if USE_CLOUD and endee_index:
                            print(f"✅ Indexed: {rel_path} (Local + Cloud)")
                        else:
                            print(f"✅ Indexed: {rel_path} (Local only)")
                except Exception as e:
                    print(f"⚠️ Skip {file}: {e}")
    print(f"--- Indexing Complete! {count} files processed. ---")

def search_code(query):
    """
    Performs semantic search: Retrieves code snippets from cloud or local DB.
    Returns results for frontend processing.
    """
    results = []
    source_db = "Local ChromaDB"
    
    # A. RETRIEVE - Try Endee Cloud first
    if USE_CLOUD and endee_index:
        try:
            print("☁️  Searching cloud index...")
            query_vector = embed_model.encode(query).tolist()
            cloud_results = endee_index.search(query_vector, top_k=4)
            
            if cloud_results and len(cloud_results) > 0:
                results = cloud_results
                source_db = "Endee Cloud"
                print(f"✅ Found {len(results)} results in cloud")
        except Exception as e:
            print(f"⚠️  Cloud search failed ({e}). Falling back to local DB...")
    
    # A. RETRIEVE - Fall back to ChromaDB if cloud failed or not available
    if not results:
        try:
            query_vector = embed_model.encode(query).tolist()
            chroma_results = collection.query(query_embeddings=[query_vector], n_results=4)
            
            if chroma_results['documents'][0]:
                # Convert ChromaDB format to match cloud format
                results = []
                for i in range(len(chroma_results['documents'][0])):
                    results.append({
                        'content': chroma_results['documents'][0][i],
                        'metadata': chroma_results['metadatas'][0][i]
                    })
                source_db = "Local ChromaDB"
                print(f"✅ Found {len(results)} results locally")
        except Exception as e:
            print(f"⚠️  Local search failed ({e})")
    
    if not results:
        print("No relevant code snippets found.")
        return None
    
    # B. BUILD RESPONSE
    response = {
        'query': query,
        'results': results,
        'source': source_db,
        'count': len(results)
    }
    
    print(f"📊 Retrieved from: {source_db}")
    return response

if __name__ == "__main__":
    # Index if the DB is empty
    local_count = collection.count()
    if local_count == 0:
        print("\n🔄 Local database is empty. Indexing codebase...")
        index_codebase(BASE_DIR)
    else:
        print(f"✅ Local database loaded with {local_count} code snippets.")

    print("\n" + "="*60)
    print("🚀 CODEBASE SEARCH ENGINE (Backend)")
    print("="*60)
    if USE_CLOUD and endee_index:
        print("☁️  Using Endee Cloud (with local fallback)")
    else:
        print("💾 Using Local ChromaDB only")
    print("Search indexed code or 'exit' to quit.")
    print("="*60)
    
    while True:
        user_input = input("\n🔍 Search your code (or 'exit') > ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        if not user_input.strip():
            continue
        
        result = search_code(user_input)
        if result:
            print(f"\n📊 Results ({result['count']} snippets found):")
            print("="*60)
            for i, item in enumerate(result['results'], 1):
                path = item.get('metadata', {}).get('path', 'unknown') if isinstance(item, dict) else 'unknown'
                content = item.get('content', str(item)) if isinstance(item, dict) else str(item)
                print(f"\n[{i}] FILE: {path}")
                print(f"CODE: {content[:500]}..." if len(content) > 500 else f"CODE: {content}")
            print("="*60)