import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# *debug
# print (api_key);

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= api_key
)
messages = []

messages.append({
    "role": "user",
    "content": "My name is Naina and I am participating in the Razorpay Buildathon."
})
response = client.chat.completions.create(
    model="openrouter/free", 
    #openrouter/free acts as a router. It can select an available free model to handle your request.
    max_tokens=500,
    temperature= 0.1,
    messages= messages
)
assistant_response = response1.choices[0].message.content

messages.append({
    "role": "assistant",
    "content": assistant_response
})

messages.append({
    "role": "user",
    "content": "Do you have any suggesstions?"
})
response1 = client.chat.completions.create(
    model="openrouter/free", 
    #openrouter/free acts as a router. It can select an available free model to handle your request.
    max_tokens=500,
    temperature= 0.1,
    messages= messages
)
print(response1.choices[0].message.content) #next chat response, not the messages array