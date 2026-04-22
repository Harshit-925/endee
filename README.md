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
| 🤖 **LLM (Brain)** | Google Gemini 3 Flash (2026 Edition) |
| 🗃️ **Vector Database (Memory)** | ChromaDB |
| 📐 **Embeddings** | `all-MiniLM-L6-v2` via Sentence-Transformers |
| 🖥️ **Frontend** | Streamlit (Modern Dark UI) |
| ⚙️ **Core Logic** | Python 3.10+, HNSWlib integration |

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
pip install google-genai chromadb sentence-transformers python-dotenv streamlit
```

### 4️⃣ Configure Your API Key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/)
2. Create a `.env` file in the project root
3. Add the following line:

```env
GEMINI_API_KEY=your_actual_key_here
```

### 5️⃣ Launch the Assistant

```bash
streamlit run ui.py
```

> 💡 **Note:** On first run, Tracr will automatically scan your folder and index your codebase. A `codebase_db/` folder will be created locally.

---

## 🔍 How It Works (Under the Hood)

```
Your Question
     │
     ▼
┌─────────────────────┐
│   Vectorization     │  ← Your question → 384-dim vector
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   HNSW Retrieval    │  ← Finds top 4 closest code chunks
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   Gemini Flash LLM  │  ← "Explain using only this specific code"
└─────────────────────┘
          │
          ▼
      Your Answer ✅
```

1. **Indexing** — Reads `.py`, `.java`, `.cpp`, `.js`, and `.h` files; breaks them into 2000-character chunks
2. **Vectorization** — Each chunk is converted into a 384-dimensional embedding
3. **Query** — Your question is also vectorized
4. **Retrieval** — HNSW algorithm finds the 4 most mathematically relevant code chunks
5. **Generation** — Gemini is instructed to answer using only those specific chunks

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

- 🏠 **Local Data** — Your code is indexed and stored entirely on your machine
- 🔒 **Safe Secrets** — `.env` is listed in `.gitignore` so API keys are never exposed
- ⚡ **Efficiency** — Automatically ignores heavy folders like `.git`, `.venv`, and `node_modules`

---

## 📐 Architecture Flow

```
┌──────────────────────────────────────────────────────────────┐
│                        TRACR RAG PIPELINE                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. USER QUERY  →  "How does the search work?"               │
│         │                                                    │
│         ▼                                                    │
│  2. EMBEDDING   →  Query converted to 384-dim Vector         │
│         │                                                    │
│         ▼                                                    │
│  3. CHROMA DB   →  Cosine Similarity search across chunks    │
│         │                                                    │
│         ▼                                                    │
│  4. RETRIEVAL   →  Top 4 most relevant code snippets         │
│         │                                                    │
│         ▼                                                    │
│  5. GEMINI 3    →  Processes [snippets + query] together     │
│         │                                                    │
│         ▼                                                    │
│  6. RESPONSE    →  Human-readable technical explanation ✅   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Technical Deep Dive

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

### 🔁 API Reliability — Exponential Backoff
To handle Gemini API rate limits gracefully, Tracr implements **Exponential Backoff with Model Fallback logic** — automatically retrying with increasing delays before switching to a fallback model, ensuring zero hard crashes under load.

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