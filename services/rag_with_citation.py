from anthropic import Anthropic
from retrieval import retrieve_chunks

anthropic_client = Anthropic()

query = "I need help to create ami"
# query="How to deploy Kubernetes on Mars?"
# query="How to cook pasta?"

results = retrieve_chunks(query)

context=""

if (len(results)>0):
  for index,result in enumerate(results):
    print("\n Vector Search Result \n", result)
    context+=f"\n\n CHUNK ID: {result.payload['chunk_index']} \n CHUNK SOURCE: {result.payload['document']} \n CHUNK {index+1}: \n {result.payload['text']}"

  prompt=f"""
  You are a helpful AI assistant. You need to answer users question from only the given context. Please also cite CHUNK ID, CHUNK SOURCE when you give the answer so user can see the proper citation sources. ONLY Cite chunks that are actually used. If you don't find anything from the given context just say 'I wasn't able to find anything in the given context' and DO NOT Hallucinate or give any wrong ANSWERS at all.

  QUESTION:
  {query}
  CONTEXT:
  {context}

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
else:
  print("I couldn't find relevant information.")
