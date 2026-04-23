# 🚀 Tracr — AI-Powered Codebase Architect

> **"Stop searching for code. Start talking to it."**

---

## 🧠 What is Tracr?

**Tracr** is a cutting-edge **Retrieval-Augmented Generation (RAG)** tool that transforms your local codebase into an interactive, intelligent assistant.

Whether you're navigating complex C++ algorithms like **HNSW** or trying to understand a massive full-stack project — Tracr finds the relevant logic and explains it to you in plain English.

---

## ❓ The Problem & The Solution

### The Problem
In large projects, finding *where* a specific logic lives is frustrating.

Standard `Ctrl+F` only works if you know the exact keyword. Searching *"How does the database save data?"* returns zero results — because the code uses terms like `persist()` or `commit()`.

### The Solution
Tracr doesn't just look at words — it understands **meaning**.

| Feature | Description |
|---|---|
| 🔍 **Semantic Search** | Converts code into mathematical "vectors" (embeddings) |
| 🏗️ **RAG Architecture** | Retrieves relevant snippets and feeds them to Gemini Flash |
| 🧩 **Contextual Intelligence** | "Reads" your specific files before answering — no hallucinations |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| 🤖 **LLM (Brain)** | Google Gemini Flash (Multi-model fallback) |
| ☁️ **Primary Vector DB** | **Endee.io Cloud** (Distributed, Scalable) |
| 💾 **Fallback Vector DB** | ChromaDB (Local Backup) |
| 📐 **Embeddings** | `all-MiniLM-L6-v2` via Sentence-Transformers (384-dim) |
| 🖥️ **Frontend** | Streamlit (Modern Dark UI) |
| ⚙️ **Backend** | Python 3.14+, Semantic Search Engine |

---

## 🚦 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/tracr.git
cd tracr
```

### 2️⃣ Set Up a Virtual Environment

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install endee langchain-endee google-generativeai chromadb sentence-transformers python-dotenv streamlit
```

### 4️⃣ Configure Your API Keys

Create a `.env` file in the project root with both Endee.io Cloud and Google Gemini credentials:

```env
# Endee.io Cloud - Vector Database (Primary)
ENDEE_API_TOKEN=your_endee_cloud_token

# Google Gemini AI - Code Explanation (Frontend)
GEMINI_API_KEY=your_gemini_api_key
```

**Setup Instructions:**
1. **Endee.io Cloud** → Register at [endee.io](https://endee.io) and create an API token
2. **Google Gemini** → Get free API key from [Google AI Studio](https://aistudio.google.com/)
3. **Create Cloud Index** → Create an index named `codebaseindex` on Endee.io dashboard
4. **Save credentials** → Add both keys to `.env`

### 5️⃣ Launch the Assistant

```bash
streamlit run ui.py
```

> 💡 **Note:** On first run, Tracr will automatically scan your folder and index your codebase. A `codebase_db/` folder will be created locally.

---

## 🔍 How It Works (Under the Hood)

### **Dual Vector Database Architecture**

```
Your Question
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│   Vectorization (SentenceTransformer - 384-dim)          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  TRY: Endee.io Cloud │ ← PRIMARY (Distributed, Fast)
        │  (codebaseindex)     │
        └──────────┬───────────┘
                   │
             FAIL? ▼
        ┌──────────────────────┐
        │ FALLBACK: ChromaDB   │ ← LOCAL (Reliable Backup)
        └──────────┬───────────┘
                   │
                   ▼
         ┌──────────────────────┐
         │ Top 4 Code Snippets  │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  Gemini Flash LLM    │ ← AI Explanation
         └──────────┬───────────┘
                    │
                    ▼
               Your Answer ✅
```

### **Indexing Pipeline**
1. **File Scanning** — Reads code files (`.py`, `.java`, `.cpp`, `.js`, `.h`, etc.)
2. **Smart Chunking** — Breaks files into 2,000-character segments for context preservation
3. **Dual Storage** — Saves embeddings to BOTH Endee.io Cloud + ChromaDB simultaneously
4. **Cloud-First Retrieval** — Queries try Endee.io first for speed; falls back to local ChromaDB if cloud unavailable

### **Query Resolution**
1. Your question is converted to a 384-dimensional vector
2. Semantic similarity search finds the 4 most relevant code chunks
3. Gemini processes the code context + your question
4. AI explanation is generated using only the retrieved code (no hallucinations)

---

## 💡 Example Questions to Ask

```
"Explain the HNSW algorithm implementation in this project."

"Where is the database connection string handled?"

"How does the error handling in app.py work?"

"Give me a summary of all the API endpoints in the src folder."
```

---

## 🛡️ Privacy & Safety

- ☁️ **Distributed Storage** — Code indexed to Endee.io Cloud for scalability and speed
- 💾 **Local Backup** — Always maintained in local ChromaDB for privacy and redundancy
- 🔄 **Automatic Fallback** — If cloud unavailable, queries seamlessly use local database
- 🏠 **Your Control** — You own your API tokens; data persists in your Endee.io account
- 🔒 **Safe Secrets** — `.env` is listed in `.gitignore` so API keys are never exposed
- ⚡ **Efficiency** — Automatically ignores heavy folders like `.git`, `.venv`, and `node_modules`

---

## 📐 Architecture Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                     TRACR RAG PIPELINE WITH ENDEE.IO                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. USER QUERY  →  "How does the search work?"                     │
│         │                                                          │
│         ▼                                                          │
│  2. EMBEDDING   →  Query converted to 384-dim Vector               │
│         │                                                          │
│         ▼                                                          │
│  3. VECTOR DB LOOKUP:                                              │
│     ├─→ PRIMARY: Endee.io Cloud (codebaseindex) ⚡                 │
│     │   (Distributed, Fast Semantic Search)                       │
│     └─→ FALLBACK: ChromaDB (Local) 💾                              │
│         (If Endee.io unavailable)                                  │
│         │                                                          │
│         ▼                                                          │
│  4. RETRIEVAL   →  Top 4 most relevant code snippets               │
│         │                                                          │
│         ▼                                                          │
│  5. GEMINI AI   →  Processes [snippets + query] together           │
│         │                                                          │
│         ▼                                                          │
│  6. RESPONSE    →  Human-readable technical explanation ✅         │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### **Data Flow: From Code to Cloud**

```
┌─────────────────────────┐
│  Your Codebase          │
│  (C++, Python, etc.)    │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────────────┐
    │  Indexing Engine       │
    │  (app.py)              │
    └────────┬────┬──────────┘
             │    │
    ┌────────▼┐  ▼────────┐
    │  Endee  │  ChromaDB │
    │  Cloud  │  (Local)  │
    │ (384-D) │  (384-D)  │
    └────────┬┘  └────────┘
             │        │
             │  Dual Indexing
             │  (Synchronized)
```

---

## ⚙️ Technical Deep Dive

### ☁️ Endee.io Cloud Integration
Tracr uses **Endee.io** as the primary vector database for production-scale semantic search:
- **Distributed Architecture** — Queries processed across multiple servers for low latency
- **384-Dimensional Vectors** — Optimized embedding size for accuracy vs. speed tradeoff
- **Automatic Indexing** — Code chunks saved to cloud index `codebaseindex` on every scan
- **Smart Fallback** — If cloud is unavailable, local ChromaDB takes over seamlessly
- **Scalability** — Cloud handles unlimited vectors; local DB keeps offline copies

### 🧩 Smart Chunking Strategy
To ensure the AI doesn't lose context, Tracr uses a **Sliding Window Chunking** approach. Each file is broken into **2000-character segments**, preventing the LLM from being overwhelmed while keeping the most relevant logic intact within a single context window.

### ⚡ Vector Space Efficiency
The `all-MiniLM-L6-v2` model generates dense **384-dimensional embeddings** — a deliberate "sweet spot" between search accuracy and processing speed. This keeps the assistant responsive even on consumer-grade hardware without sacrificing retrieval quality.

### 🛡️ Noise Reduction via Clean-Sweep Filter
The indexing engine automatically ignores irrelevant files before vectorization:

| Category | Examples Filtered |
|---|---|
| Compiled binaries | `.exe`, `.o`, `.class` |
| Lock files | `package-lock.json`, `poetry.lock` |
| Metadata folders | `.git`, `.idea`, `.vscode`, `node_modules` |

### 🔁 API Reliability — Multi-Model Fallback
To handle Gemini API rate limits gracefully, Tracr implements **Multi-Model Fallback logic**:
- Primary: `gemini-2.0-flash` (latest)
- Fallback 1: `gemini-1.5-pro` (stable)
- Fallback 2: `gemini-1.5-flash` (reliable)

This ensures zero hard crashes under load while maintaining response quality.

---

## 🗺️ Future Roadmap

- [ ] **Multi-modal Support** — Upload architecture diagrams (PNG/JPG) for the AI to explain visually
- [ ] **GitHub Integration** — Directly index any public or private repo via URL
- [ ] **Local LLM Support** — Integration with Ollama for 100% offline, fully private analysis
- [ ] **Auto-Refactoring** — Suggest code improvements and refactors directly in the UI
- [ ] **Diff-Aware Indexing** — Re-index only changed files using Git diff for faster updates

---

## 👨‍💻 Developer Note

This project was built to bridge the gap between **low-level code** and **high-level understanding**.

It is a strong demonstration of **AI Engineering**, **Vector Databases**, and **System Design thinking** — ideal for technical recruitment showcases and senior developer workflows.

> 🎯 **Resume Tip:** List this under a *"GenAI & System Design"* header and highlight:
> - *"Engineered a Vector-based Retrieval system to reduce LLM hallucination in technical contexts."*
> - *"Solved API rate-limiting via Exponential Backoff and Model Fallback logic."*

---

**Happy Coding! 🚀**