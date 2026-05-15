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
def process_document(pdf_path):
  text = extract_text_from_pdf(pdf_path)
  chunks = chunk_text(text)
  embeddings = generate_embeddings(chunks)
  document_name = os.path.basename(pdf_path)
  uploaded_chunks = upload_chunks(embeddings, document_name, chunks)
  return {
    "documents": pdf_path,
    "chunks": len(chunks),
    "status": "completed"
  }
