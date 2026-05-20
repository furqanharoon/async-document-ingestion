from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

embedding_model = SentenceTransformer(
  'all-MiniLM-L6-v2',
  local_files_only=True
)

# query = "I need help to create ami"

# encode_query = embedding_model.encode(query)

qdrant = QdrantClient(
  host="localhost",
  port=6333
)

COLLECTION_NAME = 'documents'

# results = qdrant.query_points(
#   collection_name = COLLECTION_NAME,
#   query_vector = encode_query.tolist(),
#   limit=10,
# )

MIN_SCORE = 0.65

def embed_query(query):
  return embedding_model.encode(query).tolist()

def retrieve_chunks(query):
  points = []
  search_results = qdrant.query_points(
    collection_name=COLLECTION_NAME,
    query=embed_query(query),
    limit=5
  )
  for point in search_results.points:
    if point.score >= MIN_SCORE:
      points.append(point)
  return points