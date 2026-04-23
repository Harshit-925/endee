# 🧠 Tracr: Endee.io Integration Guide

## Project Overview
**Tracr** is an AI-powered codebase analysis tool that combines:
- **Endee.io Cloud** - Distributed vector database for semantic search
- **ChromaDB** - Local fallback vector database
- **Gemini AI** - LLM for code explanation (frontend only)

---

## How Endee.io is Used

### 1️⃣ **Dual Vector Storage Architecture**

```
Your Codebase
    ↓
    ├─→ Embeddings (SentenceTransformer)
    ↓
    ├─→ Save to ChromaDB (Local) ✅
    └─→ Save to Endee Cloud ☁️
```

**What happens:**
- Code files are chunked (2000 chars per chunk)
- Each chunk → converted to embedding vector (384-dimensional)
- Vectors stored in **BOTH** places simultaneously

### 2️⃣ **Smart Retrieval with Fallback**

When user searches via Tracr UI:

```
User Query: "How does HNSW work?"
    ↓
Encode to Vector (384-dim)
    ↓
    ├─→ TRY: Search Endee Cloud (faster, distributed) ☁️
    ├─→ IF FAIL: Fall back to ChromaDB (local, reliable) 💾
    ↓
Return Top-4 Code Snippets
    ↓
Send to Gemini for AI Explanation
    ↓
Display Results + Source Files
```

### 3️⃣ **What Data is Stored**

**In Endee Cloud (`codebaseindex`):**
```json
{
  "id": "path/file.cpp_0_chunk1",
  "vector": [0.12, -0.45, 0.89, ...],  // 384 dimensions
  "document": "class HNSWIndex { ... }", // Code snippet
  "metadata": {"path": "src/hnsw/hnswlib.h"}
}
```

**In Local ChromaDB:**
Same format, but stored in `./codebase_db/`

---

## File Breakdown

### `app.py` (Backend Search Engine)
- **Function:** `search_code(query)`
- **Returns:** Structured results with file paths + code snippets
- **Process:**
  1. Encodes query to vector
  2. Tries Endee Cloud search first
  3. Falls back to ChromaDB if cloud unavailable
  4. Returns raw results (no AI processing)

### `ui.py` (Tracr Frontend)
- **Technology:** Streamlit
- **AI Name:** Tracr (not Endee)
- **Process:**
  1. Gets search results from ChromaDB
  2. Sends code context + question to Gemini
  3. Displays Gemini's explanation + source files
  4. Shows "Endee Cloud + Local DB" status

### `handshake_test.py` (Cloud Verification)
- Verifies API token is valid
- Checks cloud connection health
- Lists available indexes

---

## Current Status

### ✅ What's Working
- Local ChromaDB with 829 indexed snippets
- Semantic search (queries return relevant code)
- Backend API ready for frontend
- Handshake test confirms cloud connection
- ☁️ **Cloud index `codebaseindex` created on Endee.io!**

### ⚠️ What's Next
- Re-index codebase to populate `codebaseindex` with your code chunks
- Frontend needs valid GEMINI_API_KEY in `.env`
- Run `streamlit run ui.py` to start Tracr

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Tracr (Frontend)                       │
│                  - Streamlit Web UI                      │
│                  - User Questions                        │
│                  - Gemini Integration                    │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ↓
            ┌────────────────────────┐
            │   Backend (app.py)     │
            │  search_code(query)    │
            └────────┬───────────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
    ┌─────────────┐      ┌──────────────┐
    │  Endee      │      │   ChromaDB   │
    │  Cloud ☁️   │      │   (Local) 💾 │
    │             │      │              │
    │ Vector DB   │      │ Vector DB    │
    │ 829 chunks  │      │ 829 chunks   │
    └─────────────┘      └──────────────┘
         ↓                       ↓
    (Fast search)          (Fallback)
```

---

## Integration Points

### 1. Local Search (Always Works)
```python
# app.py
query_vector = embed_model.encode(query).tolist()
results = collection.query(query_embeddings=[query_vector], n_results=4)
```

### 2. Cloud Search (Now Active!)
```python
# app.py - Connects to 'codebaseindex' on Endee.io
if USE_CLOUD and endee_index:
    cloud_results = endee_index.search(query_vector, top_k=4)
```

### 3. AI Explanation (Frontend Only)
```python
# ui.py
response = client_ai.generate_content(full_prompt)
# Gemini processes retrieved code + user question
```

---

## Environment Variables Required

```
# .env file
GEMINI_API_KEY=your_gemini_key_here
ENDEE_API_TOKEN=your_endee_token_here
```

---

## Next Steps to Activate Cloud

1. **Verify index exists:**
   ```bash
   python handshake_test.py
   ```
   Should now show: `✅ Handshake: healthy`

2. **Re-index codebase to populate cloud:**
   ```bash
   python app.py
   ```
   This will:
   - Scan your codebase
   - Save chunks to both `codebaseindex` (cloud) and ChromaDB (local)
   - Show `☁️ Endee Cloud connected!` on startup

3. **Start Tracr frontend:**
   ```bash
   streamlit run ui.py
   ```
   Now using cloud-powered semantic search! 🚀

---

## Performance Benefits of Endee.io

| Aspect | Local ChromaDB | Endee Cloud |
|--------|---|---|
| Speed | Good (local) | Faster (distributed) |
| Scalability | Limited | Unlimited |
| Fallback | N/A | ChromaDB |
| Cost | Free | Paid (on-demand) |
| Setup | Automatic | Manual (1x) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cloud index not found" warning | Run `python app.py` to re-index (populates cloud automatically) |
| "No results found" | Re-index codebase: `python app.py` |
| "Gemini error" | Verify GEMINI_API_KEY is correct in .env |
| "Cloud connection fails" | Falls back to ChromaDB automatically (no action needed) |

---

## Summary

**Tracr** uses Endee.io as a **scalable, distributed vector database** layer on top of local ChromaDB:

- ☁️ **Endee Cloud**: For production-scale semantic search
- 💾 **ChromaDB**: For reliable local fallback
- 🧠 **Tracr Frontend**: For beautiful AI-powered code analysis

The system gracefully degrades—if cloud is unavailable, local search still works perfectly! 🚀
