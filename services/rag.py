from anthropic import Anthropic
from retrieval import retrieve_chunks

anthropic_client = Anthropic()

query = "I need help to create ami"
results = retrieve_chunks(query)

chunk_texts = []
for result in results:
  print("\n Vector Search Result \n", result)
  chunk_texts.append(result.payload['text'])

print("Chunk Texts Array", len(chunk_texts))

# STEPS:
# 1- Send Query and convert it to Vector embedding
# 2- Call retrieve chunks method and get top_k results
# 3- Get top_k chunks and append it to context and then send the context along with query and detailed system prompt to LLM

context = ""
for chunk_text in chunk_texts:
  context +=f"""\n \n {chunk_text}"""

prompt =f"""
  You're a helpful assistant. You need to answer user's query by only using the given context and if YOU DON'T FIND ANYTHING just SAY I DONT KNOW and don't give any answer on your own. Here is the given context as follows:
  {chunk_text}\n \n

  QUESTION:
  {query}
"""
response = anthropic_client.messages.create(
  max_tokens=700,
  model="claude-sonnet-4-5",
  messages=[
    {
      "role": "user",
      "content": prompt
    }
  ]
)

print("LLM RESPONSE ", response.content[0].text)

# Important RAG Learning — Retrieval Relevance vs Answer Sufficiency

## Query Used

# "I need help to create ami"

# ---

# # Observation

# The vector retrieval system successfully retrieved semantically relevant chunks related to:

# - AMI lifecycle
# - AMI creation
# - Existing AMIs
# - Creating AMIs from instances
# - EBS-backed AMIs

# Retrieval scores were also reasonable:

# - 0.75
# - 0.69
# - 0.68

# This confirmed that:
# - embeddings were functioning correctly
# - semantic search was working properly
# - vector retrieval quality was acceptable

# ---

# # Important Discovery

# Semantic retrieval quality does NOT automatically guarantee good answer generation.

# This was the first real observation of:

# ## Retrieval Relevance ≠ Context Sufficiency

# The retrieved chunks were semantically related,
# BUT they were incomplete procedural fragments.

# Examples:
# - chunks started mid-sentence
# - chunks ended abruptly
# - procedural flow was broken across chunks
# - information was fragmented

# Because of this,
# the LLM could not confidently reconstruct the full AMI creation process.

# ---

# # Very Important Observation About Claude

# Claude did NOT hallucinate missing AMI creation steps.

# Instead, it responded conservatively and stated that:
# - the context referenced AMI creation
# - but the actual complete instructions were not fully available

# This was actually a GOOD sign.

# It confirmed that:
# - grounding instructions worked correctly
# - hallucination prevention worked
# - the model respected context limitations

# ---

# # Key Insight

# The problem was NOT:

# - semantic retrieval failure

# The real problem was:

# ## insufficient contextual completeness

# This means:
# retrieved chunks were highly related,
# BUT not sufficiently composable into a coherent full procedure.

# ---

# # Why This Happens

# Current chunking system uses:

# ```python
# chunk_size = 500
# chunk_overlap = 50