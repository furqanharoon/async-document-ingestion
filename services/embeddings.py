from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
  'all-MiniLM-L6-v2',
  local_files_only=True,
)
def generate_embeddings(chunks):
  return embedding_model.encode(chunks)

def generate_single_chunk_embedding(chunk):
  embedding = embedding_model.encode(chunk)
  return embedding.tolist()