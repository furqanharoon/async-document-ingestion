from celery import Celery
import os

from services.pdf_reader import (extract_text_from_pdf)
from services.embeddings import (generate_embeddings)
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
def generate_embeddings_task(data):
  embedded_chunks = generate_embeddings(data['chunks'])
  return {
    "embeddings": embedded_chunks.tolist(),
    "chunks": data['chunks'],
    "document_name": data['document_name']
  }

@celery_app.task
def upload_vector_task(data):
  upload_chunks(data['embeddings'], data['document_name'], data['chunks'])
  return "Upload Completed"
