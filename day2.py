import os 
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = api_key
)

customer_data = {
    "cust_123": {
        "failed_attempts": 3,
        "successful_attempts": 10,
        "last_retry": "2026-08-20"
    },
    "cust_456": {
        "failed_attempts": 1,
        "successful_attempts": 5,
        "last_retry": "2026-08-21"
    }
}

def get_customer_retry_history(customer_id):
    return customer_data.get(
        customer_id,
        {"error": "Customer not found"}
    )
# print(get_customer_retry_history("cust_123"))
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_retry_history",
            "description": "Get the payment retry history for a specific customer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the customer"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
]
response = client.chat.completions.create(
    model="openrouter/free",
    max_tokens=500,
    temperature=0.1,
    tools=tools,
    messages=[
        {
            "role": "user",
            "content": "Get me the payment history of cust_123. Use the available tool."
        }
    ]
)
message = response.choices[0].message
tool_call = message.tool_calls[0]

arguments = json.loads(tool_call.function.arguments)
customer_id = arguments["customer_id"]

result = get_customer_retry_history(customer_id)

messages = [
    {
        "role": "user",
        "content": "Get me the payment history of cust_123. Use the available tool."
    },
    
    message,
    
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result)
    }
]

final_response = client.chat.completions.create(
    model="openrouter/free",
    max_tokens=100,
    temperature=0.1,
    tools=tools,
    messages=messages
)

print(final_response.choices[0].message.content)