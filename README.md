# 🚀 AI Technical Documentation Assistant
### *Vector-Powered Semantic Search for Modern Developers*

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Storage-blueviolet?style=for-the-badge)
![AI-Embeddings](https://img.shields.io/badge/AI-Sentence--Transformers-green?style=for-the-badge)

## 📖 Overview
This project is an **Intelligent Documentation Assistant** developed for the **Endee.io Placement Drive**. It leverages Retrieval-Augmented Generation (RAG) principles to provide context-aware search results.

Unlike traditional keyword search, this system uses **Deep Learning Embeddings** to understand the "intent" behind a query.

### Key Features:
* **Semantic Intent:** Recognizes that "How do I start the app?" relates to "mvn spring-boot:run".
* **Vector Persistence:** Data is stored in a local vector database for fast, efficient retrieval.
* **High Confidence Matching:** Uses Cosine Similarity to rank the best technical answers.

---

## 🏗️ System Architecture
The assistant operates in a three-stage pipeline to ensure high-accuracy retrieval:

1.  **Embedding Generation:** Utilizing the `all-MiniLM-L6-v2` model to transform raw text into 384-dimensional dense vectors.
2.  **Vector Ingestion:** Storing documents and metadata within a high-performance vector storage layer.
3.  **Real-time Retrieval:** User queries are vectorized on-the-fly and matched against the database using distance-based similarity.



---

## 🚀 Getting Started

### **1. Setup Environment**
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt

## 🧠 How it Works: Under the Hood

### **Semantic Understanding**
Traditional search engines look for **words**. This assistant looks for **meaning**. 
* **The Model:** We use `all-MiniLM-L6-v2`, which is a Siamese BERT-network. It maps sentences to a 384-dimensional dense vector space.
* **Vector Database:** When a query is made, ChromaDB calculates the **L2 Distance** (Euclidean distance) between the query vector and the stored document vectors. 
* **The Result:** The document with the smallest distance (closest meaning) is returned to the user.

## 📊 Sample Execution
When you run `python app.py`, the system performs the following:

```text
Loading AI model...
Adding knowledge to the database...
Searching for: 'How do I run a spring boot project?'

--- Search Result ---
Closest Match: To start a Spring Boot app, use the command: mvn spring-boot:run
Confidence Score: 0.60015
--- Project Complete! ---

#### **3. A "Future Roadmap" Section**
This shows you have "product vision." 

```markdown
## 🛠️ Future Enhancements
- [ ] **Web Interface:** Wrap this logic in a Flask or FastAPI backend with a React frontend.
- [ ] **Multi-Document Support:** Add a PDF parser to allow the assistant to read entire manuals.
- [ ] **LLM Integration:** Connect the retrieved context to an LLM (like GPT-4 or Gemini) to generate human-like conversational answers.