from services.rag_with_conversational_history import generate_rag_response

conversation_history = []

# while(True):
# user_query = input("\n User:")
# if user_query.lower() == 'exit':
#   break
user_query = "How do I create an AMI?"

print("INPUT: \n", user_query)

response = generate_rag_response(user_query, conversation_history=conversation_history)
print("LLM Response: \n", response)
conversation_history.append(
  {
    "role":"user",
    "content": user_query
  }
)
conversation_history.append(
  {
    "role": "assistant",
    "content": response
  }
)
