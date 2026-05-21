from anthropic import Anthropic
from services.retrieval import retrieve_chunks
# services
anthropic_client = Anthropic()

def generate_rag_response(query,conversation_history=None):
  history_text=""
  if conversation_history:
    for message in conversation_history:
      history_text+=f"\n\n {message['role']: message['content']}"
  
  retrieval_query =f"""
    Conversation History:
    {history_text}
    Query:
    {query}
  """
  retrieved_chunks = retrieve_chunks(retrieval_query, 5)
  print("retrieved_chunks", retrieved_chunks)
  if not retrieved_chunks:
    return "I couldn't find anything in retrieved chunks."
  
  context=""
  for index,result in enumerate(retrieved_chunks):
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
  return response.content[0].text
  