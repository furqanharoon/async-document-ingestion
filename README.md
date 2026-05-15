# Async Document Ingestion Pipeline

Production-style asynchronous AI document ingestion pipeline using Celery, Redis, Sentence Transformers, and Qdrant.

This project demonstrates how modern AI systems process large document workloads using:
- background workers
- queues
- async task execution
- embedding pipelines
- vector database ingestion

---

# Architecture

```text
Client / API
↓
Celery Task Queue
↓
Redis Broker
↓
Celery Worker
↓
PDF Extraction
↓
Chunking
↓
Embedding Generation
↓
Qdrant Vector Storage
```

---

# Features

- Async PDF ingestion
- Celery background workers
- Redis task queue
- PDF text extraction
- Text chunking
- Embedding generation
- Qdrant vector ingestion
- Modular AI pipeline architecture

---

# Tech Stack

- Python
- Celery
- Redis
- Sentence Transformers
- Qdrant
- PyMuPDF

---

# Why Async Ingestion?

Traditional synchronous ingestion pipelines block application requests while processing large documents.

This project moves heavy AI workloads into background workers using Celery queues, enabling:
- non-blocking ingestion
- scalable processing
- distributed workloads
- better fault isolation
- async orchestration

---

# Learning Goals

This repository was built to deeply understand:

- queue-based architectures
- async task execution
- worker systems
- ingestion orchestration
- vector database pipelines
- distributed AI infrastructure concepts

---

# Project Structure

```text
async-document-ingestion/
│
├── main.py
├── tasks.py
├── qdrant_setup.py
│
├── services/
│   ├── pdf_reader.py
│   ├── chunker.py
│   ├── embeddings.py
│   └── vector_store.py
│
└── documents/
```

---

# Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Start Redis

```bash
brew services start redis
```

Verify:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

---

# Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

# Create Qdrant Collection

```bash
python qdrant_setup.py
```

---

# Start Celery Worker

```bash
celery -A tasks worker --pool=solo --loglevel=info
```

Note:
`--pool=solo` is used for development stability on macOS with ML libraries like PyTorch/SentenceTransformers.

---

# Run Ingestion

```bash
python main.py
```

---

# Example Worker Output

```text
Task tasks.process_document[...] succeeded in 1.76s

{
  "document": "file1.pdf",
  "chunks": 199,
  "status": "completed"
}
```

---

# Current Limitations

- Single-stage ingestion task
- No retry policies yet
- No distributed task chaining yet
- No observability dashboard yet
- Chunk IDs are not globally unique yet

---

# Future Improvements

- Multi-stage Celery task pipelines
- Retry handling
- Dead-letter queues
- Worker concurrency scaling
- Observability + metrics
- Streaming ingestion
- Distributed orchestration
- Cloud storage ingestion (S3/GCS)

---

# Key Concepts Learned

- Queues
- Workers
- Async execution
- Ingestion orchestration
- Background job systems
- Distributed processing
- Vector ingestion pipelines
- AI infrastructure fundamentals

---

# License

MIT
