from dotenv import load_dotenv
import os
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer('all-MiniLM-L6-v2') # 384 Embedding size

text = "Machince Learning is fun."

embedding = model.encode(text)

print(f"Text: {text}")
print(f"Embedding: {embedding[:10]}")  # Print first 10 dimensions of the embedding
print(f"Embedding shape: {embedding.shape}")
