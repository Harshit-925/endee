import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the AI Model
print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Setup the Vector Database (Local)
# This creates a folder on your computer to act as the DB
client = chromadb.PersistentClient(path="./my_vector_db")
collection = client.get_or_create_collection(name="tech_docs")

# 3. Your Knowledge Data
docs = [
    "To start a Spring Boot app, use the command: mvn spring-boot:run",
    "Java interfaces define a contract that classes must implement.",
    "The @RestController annotation in Spring marks a class as a web handler.",
    "Use 'git clone' to download a repository from GitHub to your computer."
]

# 4. Add data to the Database
print("Adding knowledge to the database...")
embeddings = model.encode(docs).tolist()
ids = [f"id_{i}" for i in range(len(docs))]

collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=ids
)

# 5. Perform the Search
query = "How do I run a spring boot project?"
print(f"\nSearching for: '{query}'")

query_embedding = model.encode(query).tolist()
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

print("\n--- Search Result ---")
print(f"Closest Match: {results['documents'][0][0]}")
print(f"Confidence Score: {results['distances'][0][0]}")

print("\n--- Project Complete! ---")