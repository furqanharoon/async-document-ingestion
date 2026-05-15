from qdrant_client import QdrantClient
from qdrant_client.models import (VectorParams, Distance)

qdrant=QdrantClient(
  host="localhost",
  port=6333
)
qdrant.create_collection(
  collection_name="documents",
  vectors_config=VectorParams(
    size=384,
    distance=Distance.COSINE
  )
)
print("Collection created")
