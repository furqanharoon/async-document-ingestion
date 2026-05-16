from tasks import (extract_text_pdf_task, get_chunks_task, upload_vector_task, generate_embeddings_parallel_task)
from celery import chain

# result = process_document.delay("../documents/small_size_pdfs/file1.pdf")
# print ('\n Result :\n', result)
file_path = "../documents/small_size_pdfs/file1.pdf"
workflow = chain(
  extract_text_pdf_task.s(file_path),
  get_chunks_task.s(),
  generate_embeddings_parallel_task.s(),
  upload_vector_task.s()
)
workflow.delay()
print('Workflow', workflow)
