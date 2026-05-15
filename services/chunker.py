def chunk_text(text,chunk_size=500,chunk_overlap=50):
  print("chunk_text")
  chunks = []
  start = 0
  while(start < len(text)):
    end = start + chunk_size
    chunk = text[start:end]
    chunks.append(chunk)
    start = end - chunk_overlap
  return chunks
