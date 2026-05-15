from celery import Celery

celery_app = Celery(
  "tasks",
  broker="redis://localhost:6379/0",
  backend="redis://localhost:6379/0"
)

@celery_app.task
def process_document(pdf_path):
  print("process_documend called")
