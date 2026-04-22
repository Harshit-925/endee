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