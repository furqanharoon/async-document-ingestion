from anthropic import Anthropic
from retrieval import retrieve_chunks
from sentence_transformers import CrossEncoder

anthropic_client = Anthropic()

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def generate_rag_response(query,conversation_history=None):
  retrieved_chunks = retrieve_chunks(query, 15)
  if not retrieved_chunks:
    return "I couldn't find anything in retrieved chunks."
  
  candidate_pairs= []
  for result in retrieved_chunks:
    candidate_pairs.append([
      query,
      result.payload['text']
    ])
  
  rerank_scores = reranker.predict(candidate_pairs)
  # reranked_results = list(zip(retrieved_chunks, rerank_scores))
  reranked_results = []
  for result,rerank_score in zip(retrieved_chunks, rerank_scores):
    reranked_results.append({
      "score": rerank_score,
      "text": result.payload['text'],
      "chunk_index": result.payload['chunk_index'],
      "document": result.payload['document']
    })
  reranked_results.sort(key=lambda x:x['score'], reverse=True)
  print("reranked_results", reranked_results)
  context=""
  for index,result in enumerate(reranked_results):
    context+=f"\n\n CHUNK ID: {result['chunk_index']} \n CHUNK SOURCE: {result['document']} \n CHUNK {index+1}: \n {result['text']}"
  print("CONTEXTTTT", context)
  
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

generate_rag_response("How to create an AMI")