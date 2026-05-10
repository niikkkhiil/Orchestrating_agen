import os 
import json
import faiss
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

# Embedding model for vectorizing text
model = SentenceTransformer('all-MiniLM-L6-v2')

# Storage path for memory
MEMORY_DIR = os.path.join(os.path.dirname(__file__),"../../memory")
INDEX_PATH = os.path.join(  MEMORY_DIR, "incidents.index")
DATA_PATH = os.path.join(MEMORY_DIR, "incidents.json")


# Create memory folder if dosnt exist
os.makedirs(MEMORY_DIR, exist_ok=True)

# Vector Dimension for the embedding model
DIMENSION = 384
SIMILARITY_THRESHOLD = 0.85

def _load_index():
    """Load existing FAISS index or create a new one."""
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return faiss.IndexFlatL2(DIMENSION)


def _load_data():
    """Load existing incident records or return empty list."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []


def _save_index(index):
    """Save FAISS index to disk."""
    faiss.write_index(index, INDEX_PATH)


def _save_data(data):
    """Save incident records to disk."""
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def search_memory(container_name: str, logs: str) -> dict | None:
    """
    Search FAISS for similar past incidents.
    Returns the past fix if similarity is above threshold, else None.
    """
    index = _load_index()
    data = _load_data()

    if index.ntotal == 0:
        return None

    # Create search query from container + logs
    query = f"Container: {container_name}\nLogs: {logs[:500]}"
    query_vector = model.encode([query]).astype("float32")

    # Search top 1 most similar incident
    distances, indices = index.search(query_vector, 1)

    best_distance = distances[0][0]
    best_index = indices[0][0]

    # Lower distance = more similar (L2 distance)
    # Convert to similarity score
    similarity = 1 / (1 + best_distance)

    if similarity >= SIMILARITY_THRESHOLD and best_index < len(data):
        match = data[best_index]
        print(f"\n Memory hit! Similar incident found (similarity: {similarity:.2f})")
        print(f"   Past incident: {match['container_name']} at {match['timestamp']}")
        print(f"   Known fix: {match['fix']}")
        return match

    return None


def save_to_memory(container_name: str, logs: str, diagnosis: str, fix: str):
    """
    Save a new incident to FAISS memory.
    """
    index = _load_index()
    data = _load_data()

    # Create vector from incident
    text = f"Container: {container_name}\nLogs: {logs[:500]}"
    vector = model.encode([text]).astype("float32")

    # Add to FAISS index
    index.add(vector)

    # Save incident details
    incident = {
        "container_name": container_name,
        "logs_preview": logs[:500],
        "diagnosis": diagnosis,
        "fix": fix,
        "timestamp": datetime.now().isoformat()
    }
    data.append(incident)

    # Persist to disk
    _save_index(index)
    _save_data(data)

    print(f"\n Incident saved to memory: {container_name}")
    print(f"   Total incidents in memory: {len(data)}")


def get_memory_stats() -> str:
    """Returns a summary of what's in memory."""
    data = _load_data()
    if not data:
        return "Memory is empty — no incidents recorded yet."

    stats = f"Total incidents in memory: {len(data)}\n"
    for i, incident in enumerate(data[-5:], 1):
        stats += f"{i}. {incident['container_name']} at {incident['timestamp']}\n"
    return stats