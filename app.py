import requests
from sentence_transformers import SentenceTransformer
import time

# 1. Load the AI Model
print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Knowledge Base
docs = [
    "To start a Spring Boot app, use the command: mvn spring-boot:run",
    "Java interfaces define a contract that classes must implement.",
    "The @RestController annotation in Spring marks a class as a web handler.",
    "Use 'git clone' to download a repository from GitHub to your computer."
]

ENDEE_URL = "http://localhost:8080"

# 3. Adding knowledge
print("Adding knowledge to Endee...")
for i, text in enumerate(docs):
    vector = model.encode(text).tolist()
    payload = {
        "id": str(i),
        "vector": vector,
        "metadata": {"content": text}
    }
    
    # Try the 'endee' default collection path
    response = requests.post(f"{ENDEE_URL}/api/v1/endee/insert", json=payload)
    print(f"Status for doc_{i}: {response.status_code}")

time.sleep(1)

# 4. Search
query = "How do I run a spring boot project?"
print(f"\nSearching for: '{query}'")

query_vector = model.encode(query).tolist()
search_payload = {"vector": query_vector, "top_k": 1}

try:
    # Try the 'endee' default collection path
    response = requests.post(f"{ENDEE_URL}/api/v1/endee/search", json=search_payload)
    print("Match Found:", response.text)
except Exception as e:
    print("Search failed. Error:", e)

print("\n--- Project Complete! ---")