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
INDEC_PATH = os.path.join(  MEMORY_DIR, "incidents.index")
DATA_PATH = os.path.join(MEMORY_DIR, "incidents.json")


# Create memory folder if dosnt exist
os.makedirs(MEMORY_DIR, exist_ok=True)

# Vector Dimension for the embedding model
VECTOR_DIM = 384
SIMILARITY_THRESHOLD = 0.7

