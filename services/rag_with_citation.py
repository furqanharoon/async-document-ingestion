from anthropic import Anthropic
from retrieval import retrieve_chunks

anthropic_client = Anthropic()

# query = "I need help to create ami"
query="How to deploy Kubernetes on Mars?"

results = retrieve_chunks(query)

# chunk_texts = []
context=""

for index,result in enumerate(results):
  print("\n Vector Search Result \n", result)
  context+=f"\n\n CHUNK ID: {result.payload['chunk_index']} \n CHUNK SOURCE: {result.payload['document']} \n CHUNK {index+1}: \n {result.payload['text']}"

print("CONTEXTTTTT", context)

prompt=f"""
You are a helpful AI assistant. You need to answer users question from only the given context. Please also cite CHUNK ID, CHUNK SOURCE when you give the answer so user can see the proper citation sources. ONLY Cite chunks that are actually used. If you don't find anything from the given context just say 'I wasn't able to find anything in the given context' and DO NOT Hallucinate or give any wrong ANSWERS at all.

QUESTION:
{query}
CONTEXT:
{context}

"""

# chunk_texts.append(result)

# print("Chunk Texts Array", len(chunk_texts))

# STEPS:
# 1- Send Query and convert it to Vector embedding
# 2- Call retrieve chunks method and get top_k results
# 3- Get top_k chunks and append it to context and then send the context along with query and detailed system prompt to LLM

# context = ""
# for index, chunk_text in enumerate(chunk_texts):
#   context += f"\n\n CHUNK {index+1}: \n {chunk_text}"
# print("\n CONTEXT \n", context)

# prompt=f"""
# You are a helpful AI assistant. You need to look only into the context and help users find answer to their question. If you don't find any Answer in the context, just say 'I wasn't able to find anything from the given context'. DO NOT HALLUCINATE or give any wrong answers.

# Context:
# {context}

# Question:
# {query}
# """
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