from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

def upload_chunks(embedded_chunks, chunks, document_name):
  qdrant = QdrantClient(
    host="localhost",
    port=6333
  )
  COLLECTION_NAME = "documents"
  
  BATCH_SIZE=100

  for batch_start in range(
    0,
    len(chunks),
    BATCH_SIZE
  ):
    points = []
    batch_chunks = chunks[batch_start:batch_start + BATCH_SIZE]

    batch_embeddings = embedded_chunks[batch_start:batch_start + BATCH_SIZE]

    for index,(chunk,embedding) in enumerate(zip(batch_chunks, batch_embeddings)):
      point = PointStruct(
        id=batch_start+index,
        vector=embedding,
        payload = {
          "text": chunk,
          "document": document_name,
          "chunk_index":batch_start + index
        }
      )
      points.append(point)
    qdrant.upsert(
      collection_name=COLLECTION_NAME,
      points=points
    )
