from celery import Celery
from celery import group

import os

from services.pdf_reader import (extract_text_from_pdf)
from services.embeddings import (generate_embeddings, generate_single_chunk_embedding)
from services.chunker import (chunk_text)
from services.vectore_store import (upload_chunks)

celery_app = Celery(
  "tasks",
  broker="redis://localhost:6379/0",
  backend="redis://localhost:6379/0"
)

@celery_app.task
def extract_text_pdf_task(file_path):
  text = extract_text_from_pdf(file_path)
  document_name = os.path.basename(file_path)
  return {
    "text":text,
    "document_name": document_name
  }

@celery_app.task
def get_chunks_task(data):
  chunks = chunk_text(data['text'])
  return {
    "chunks": chunks,
    "document_name": data['document_name']
  }

@celery_app.task
def generate_embedding_task(chunk):
  embedding = generate_single_chunk_embedding(chunk)
  return {
    "chunk": chunk,
    "embedding": embedding
  }

@celery_app.task
def generate_embeddings_parallel_task(data):
  chunks = data['chunks']
  document_name = data['document_name']
  embedding_group = group(
    generate_embedding_task.s(chunk)
    for chunk in chunks
  )
  results = embedding_group.apply_async()
  embedding_results = results.get()
  return {
    "embedding_results": embedding_results,
    "document_name": document_name
  }

@celery_app.task
def upload_vector_task(data):
  # upload_chunks(data['embeddings'], data['document_name'], data['chunks'])
  # return "Upload Completed"
  chunks = []
  embeddings = []

  for embedding_result in data['embedding_results']:
    embeddings.append(embedding_result['embedding'])
    chunks.append(embedding_result['chunk'])
  
  upload_chunks(embeddings, data['document_name'], chunks)
  return "Upload Completed"

