import os
import json
import time
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

# 1. Open the .env safe
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# 2. Setup Google GenAI Client
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)


# 3. Create a custom tool that translates text into numbers (Vectors) using Gemini
class GeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        embeddings = []
        for text in input:
            response = client.models.embed_content(
                model="gemini-embedding-001", contents=text
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings


def build_vector_db():
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "raw_jira_tickets.json"
    db_dir = base_dir / "data" / "chroma_db"

    print("Reading Jira tickets from JSON...")
    try:
        with open(data_file, "r") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {data_file}. Did you run ingest_jira.py?")
        return

    documents = []
    metadatas = []

    for ticket in tickets:
        # --- NEW: METADATA EXTRACTION ENGINE ---
        # We split the summary by ":" to find the Tricode and Platform
        summary = ticket.get("summary", "")
        parts = summary.split(":")

        # Safely grab the tricode and platform if they follow the YinzCam standard
        tricode = parts[0].strip() if len(parts) > 0 else "UNKNOWN"
        platform = parts[1].strip() if len(parts) > 1 else "UNKNOWN"

        # Combine everything for the AI to read
        content = f"Ticket Key: {ticket['key']}\nType: {ticket['type']}\nSummary: {summary}\nDescription: {ticket['description']}"
        documents.append(content)

        # --- NEW: ATTACHING THE SMART TAGS ---
        metadatas.append(
            {
                "key": ticket.get("key", "UNKNOWN"),
                "type": ticket.get("type", "UNKNOWN"),
                "tricode": tricode,  # Allows us to filter by App
                "platform": platform,  # Allows us to filter by team/tech
            }
        )

    print("Initializing ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=str(db_dir))

    try:
        chroma_client.delete_collection(name="jira_memory")
    except Exception:
        pass

    collection = chroma_client.create_collection(
        name="jira_memory", embedding_function=GeminiEmbeddingFunction()
    )

    print("Chopping tickets into smaller chunks for the AI...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    chunked_docs = []
    chunked_metas = []
    chunked_ids = []

    for i, doc in enumerate(documents):
        chunks = text_splitter.split_text(doc)
        for j, chunk in enumerate(chunks):
            chunked_docs.append(chunk)
            chunked_metas.append(metadatas[i])
            chunked_ids.append(f"{metadatas[i]['key']}_chunk_{j}")

    print(f"Total chunks to insert: {len(chunked_docs)}")
    print("Translating to vectors and saving to database... (This might take a minute)")

    batch_size = 10
    for i in range(0, len(chunked_docs), batch_size):
        batch_docs = chunked_docs[i : i + batch_size]
        batch_metas = chunked_metas[i : i + batch_size]
        batch_ids = chunked_ids[i : i + batch_size]

        collection.add(documents=batch_docs, metadatas=batch_metas, ids=batch_ids)
        print(
            f" -> Processed batch {(i//batch_size) + 1} / {(len(chunked_docs)//batch_size) + 1}"
        )
        time.sleep(1.5)

    print("\n✅ Vector Database built successfully with advanced Metadata Routing!")

    # ---------------------------------------------------------
    # TEST: Let's do a quick search to prove it works
    # ---------------------------------------------------------
    test_query = "What is the status of our frontend tasks?"
    print(f"\nRunning test search for: '{test_query}'")

    results = collection.query(
        query_texts=[test_query],
        n_results=2,
    )

    print("\nTop Matches Found:")
    if results["metadatas"] and results["metadatas"][0]:
        for metadata in results["metadatas"][0]:
            print(
                f" - Matched Ticket: {metadata.get('key')} | App: {metadata.get('tricode')} | Platform: {metadata.get('platform')}"
            )
    else:
        print(" - No matches found.")


if __name__ == "__main__":
    build_vector_db()
