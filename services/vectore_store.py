from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

qdrant = QdrantClient(
  host="localhost",
  port=6333
)
COLLECTION_NAME = "documents"

points = []

def upload_chunks(embedded_chunks, document_name, chunks):
  
  for index,(chunk,embedding) in enumerate(zip(chunks, embedded_chunks)):
    point = PointStruct(
      id=index,
      vector=embedding.tolist(),
      payload = {
        "text": chunk,
        "document": document_name,
        "chunk_index":index
      }
    )
    points.append(point)
  
  qdrant.upsert(
    collection_name=COLLECTION_NAME,
    points=points
  )
