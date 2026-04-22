AI-Powered Technical Documentation Assistant
Built for the Endee.io Placement Drive (Batch 2027)
📌 Project Overview
This project is a Semantic Search Assistant designed to help developers find information within technical documentation. Unlike traditional keyword search, this system uses Vector Embeddings to understand the "intent" behind a query. For example, it understands that "How do I run a project?" is related to "mvn spring-boot:run" even if the words don't match exactly.

Key Features:
Vector Database Integration: Powered by Endee OSS for high-performance vector retrieval.

AI-Driven Embeddings: Uses the all-MiniLM-L6-v2 model to convert text into 384-dimensional vectors.

RAG Architecture: Implements the core logic of Retrieval-Augmented Generation.

🏗️ System Architecture
The system follows a professional AI workflow:

Ingestion: Technical docs are "chunked" and converted into vectors.

Storage: Vectors and metadata are stored in the Endee Vector DB.

Retrieval: User queries are vectorized and matched against the database using Cosine Similarity.

🛠️ Tech Stack
Language: Python 3.x

Database: Endee Vector DB (Dockerized)

AI Libraries: sentence-transformers, PyTorch

API Handling: Requests

🚀 Getting Started
1. Prerequisite: Start Endee Server
Ensure you have Docker installed and run the following command to start the database:

PowerShell
docker run -d -p 8080:8080 --name endee-server endeeio/endee-server:latest
2. Install Dependencies
PowerShell
pip install -r requirements.txt
3. Run the Assistant
PowerShell
python app.py
🔍 Technical Challenges & Debugging
During development, I encountered and resolved several SDE-level challenges:

Environment Configuration: Successfully deployed the Endee engine using Docker on Windows, troubleshooting initial build-from-source errors by switching to the official image.

API Routing: Investigated 405 Method Not Allowed errors using docker logs. Verified connectivity via the /api/v1/health endpoint and adapted the Python client to match the server's expected RESTful namespaces.

Data Integrity: Handled JSONDecodeError by implementing robust response-handling logic to manage different API return types (JSON vs. Plain Text).

📁 Project Structure
app.py: Main logic for embedding generation, database upsertion, and searching.

requirements.txt: List of necessary Python libraries.

README.md: Documentation of the system and development process.