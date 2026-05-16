from celery import Celery
from celery import group
from celery import chord
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
  embedding_tasks = group(
    generate_embedding_task.s(chunk)
    for chunk in chunks
  )
  # Chord works like this:
  # chord(header)(callback)
  # The header means the tasks that needs to finish first. they are usually Parallel tasks. The 'callback' means the tasks that will after header tasks are complete.
  workflow = chord(
    embedding_tasks
  )(
    upload_vector_task.s(document_name)
  )
  return workflow.id



@celery_app.task(
  autoretry_for=(Exception,),
  retry_kwargs={"max_retries": 15},
  retry_backoff=True
  # This is exponential back-off. The retry time exponentially increases
  # Retry 1 → wait 10s
  # Retry 2 → wait 20s
  # Retry 3 → wait 40s
  # Retry 4 → wait 80s
)
def upload_vector_task(embedding_results, document_name):
  chunks = []
  embeddings = []
  for result in embedding_results:
    embeddings.append(result['embedding'])
    chunks.append(result['chunk'])
  upload_chunks(embeddings, chunks, document_name)
  return "Upload Completed"
