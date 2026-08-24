import os 
from dotenv import load_dotenv
from openai import OpenAI
from structured_output import decision_schema, RecoveryDecision
import json
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = api_key
)
customer_data = {
    "failed_attempts": 2,
    "successful_attempts": 10,
    "last_retry_minutes_ago": 20,
    "failure_reason": "network timeout"
} 

tools = [
    {
        "type": "function",
        "function": {
            "name": "make_recovery_decision",
            "description": (
                "Analyze the payment failure context and choose "
                "the appropriate recovery action."
            ),
            "parameters": decision_schema
        }
    }
]

messages = [
    {
        "role": "system",
        "content": """
            You are a payment recovery decision agent.

            Analyze the payment context and choose exactly one recovery action.

            Use the make_recovery_decision tool to return your decision.

            Rules:
            - Choose only an appropriate action based on the provided context.
            - Give a concise reason.
            - Only provide retry_after_minutes when the action is retry.
            """
    },
    {
        "role": "user",
        "content": json.dumps(customer_data)
    }
]

response = client.chat.completions.create(
    model="openrouter/free",
    max_tokens= 500,
    tools=tools,
    # tool_choice= "required",
    messages=messages
)

message = response.choices[0].message

tool_call = message.tool_calls[0]
arguments = json.loads(
    tool_call.function.arguments
)
decision = RecoveryDecision(**arguments)
def check_policy(decision: RecoveryDecision, customer_data: dict):

    if decision.action == "retry":

        if customer_data["failed_attempts"] >= 5:
            return False, "Maximum retry attempts reached"

        if decision.retry_after_minutes < 30:
            return False, "Retry delay must be at least 30 minutes"

        if decision.confidence < 0.7:
            return False, "Confidence is too low for automatic retry"

    return True, "Decision approved"

def execute_recovery_decision(decision: RecoveryDecision):

    if decision.action == "retry":
        print(
            f"Retrying payment after "
            f"{decision.retry_after_minutes} minutes"
        )

    elif decision.action == "notify":
        print(
            "Notifying the customer about the payment failure"
        )

    elif decision.action == "escalate":
        print(
            "Escalating the payment issue for manual review"
        )

    elif decision.action == "stop":
        print(
            "Stopping further recovery attempts"
        )

is_allowed, response = check_policy(
    decision,
    customer_data
)
print(response)
if is_allowed:
    execute_recovery_decision(decision)
else :
    print("Blocked by policy.\n")