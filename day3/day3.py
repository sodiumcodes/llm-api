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
test_cases = [
    {
        "name": "Temporary network failure",
        "data": {
            "failed_attempts": 1,
            "successful_attempts": 15,
            "last_retry_minutes_ago": 60,
            "failure_reason": "network timeout"
        }
    },
    {
        "name": "Insufficient funds",
        "data": {
            "failed_attempts": 3,
            "successful_attempts": 8,
            "last_retry_minutes_ago": 60,
            "failure_reason": "insufficient funds"
        }
    },
    {
        "name": "Ambiguous failure",
        "data": {
            "failed_attempts": 2,
            "successful_attempts": 5,
            "last_retry_minutes_ago": 90,
            "failure_reason": "unknown error"
        }
    },
    {
        "name": "Repeated failures",
        "data": {
            "failed_attempts": 6,
            "successful_attempts": 1,
            "last_retry_minutes_ago": 120,
            "failure_reason": "payment repeatedly declined"
        }
    },
    {
        "name": "Suspicious inconsistent payment state",
        "data": {
            "failed_attempts": 4,
            "successful_attempts": 20,
            "last_retry_minutes_ago": 45,
            "failure_reason": "payment status inconsistent across systems"
        }
    }
]

#the tool schema contains the action values, but the schema defines valid output—not business meaning.
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

system_prompt = """
                ## Role

                You are an AI-powered payment recovery decision agent.

                Your responsibility is to analyze failed payment situations and
                recommend the most appropriate recovery action.

                ## Objective

                Your goal is to maximize the probability of recovering a failed payment
                while minimizing unnecessary retries and customer friction.

                ## Available Actions

                You must choose exactly one of the following actions:

                - retry
                - notify
                - escalate
                - stop

                ## Decision Factors

                Consider all relevant information provided in the payment context,
                including:

                - Number of failed attempts
                - Number of successful attempts
                - Time since the last retry
                - Failure reason

                ## Action Guidelines

                Choose retry when the failure appears temporary and another payment
                attempt is reasonably likely to succeed.

                Choose notify when customer action or intervention is likely required.

                ### Handling Ambiguous Failures

                    If the failure reason is unknown or ambiguous, prefer retry when:

                    - The customer has a positive successful payment history.
                    - The number of failed attempts is low.
                    - The retry cooldown period has passed.

                    Prefer escalate when:

                    - The failure reason is unknown and there are repeated failures.
                    - The available information is insufficient to determine whether another retry is safe.
                    - The situation appears unusual or inconsistent.

                Choose stop when repeated recovery attempts are unlikely to succeed or
                further retries may create unnecessary customer friction.

                ## Constraints

                - Never invent customer or payment information.
                - Base your decision only on the provided payment context.
                - Choose exactly one allowed action.
                - Give a concise reason for the decision.
                - Only provide retry_after_minutes when the action is retry.
                
                ## Examples

                ### Example 1: Temporary technical failure

                Payment context:

                - Failed attempts: 1
                - Successful attempts: 15
                - Last retry: 60 minutes ago
                - Failure reason: network timeout

                Decision:

                - Action: retry
                - Retry after: 30 minutes

                Reason:
                The failure appears temporary and the customer has a strong successful
                payment history, so another retry is reasonably likely to succeed.


                ### Example 2: Customer action required

                Payment context:

                - Failed attempts: 3
                - Successful attempts: 8
                - Last retry: 60 minutes ago
                - Failure reason: insufficient funds

                Decision:

                - Action: notify
                - Retry after: None

                Reason:
                Another automated retry is unlikely to resolve insufficient funds
                without customer intervention.


                ### Example 3: Repeated failures

                Payment context:

                - Failed attempts: 6
                - Successful attempts: 1
                - Last retry: 120 minutes ago
                - Failure reason: payment repeatedly declined

                Decision:

                - Action: stop
                - Retry after: None

                Reason:
                Repeated payment failures and a weak successful payment history suggest
                that further automated retries are unlikely to succeed and may create
                unnecessary customer friction.
                ## Tool Usage

                You must use the make_recovery_decision tool to return the final decision.
            """

def run_agent(customer_data):
    messages = [
        {
            "role": "system",
            "content": system_prompt
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
        tool_choice= "required",
        messages=messages
    )

    message = response.choices[0].message
    if not message.tool_calls : 
        print("\n========== NO TOOL CALL ==========")
        print("Model content:")
        print(message.content)

        print("\nFull message:")
        print(message)
        print("\n")
        return None
    tool_call = message.tool_calls[0]
    arguments = json.loads(
        tool_call.function.arguments
    )
    decision = RecoveryDecision(**arguments)
    return decision

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

for test_case in test_cases:
    print(test_case["name"])
    customer_data = test_case["data"]
    decision = run_agent(customer_data)
    if decision is None:
        print("\nSkipping this test case because no tool call was returned.")
        continue

    is_allowed, response = check_policy(
        decision,
        customer_data
    )

    print("\n========== AGENT DECISION ==========")
    print(f"Action: {decision.action}")
    print(f"Retry after: {decision.retry_after_minutes}")
    print(f"Reason: {decision.reason}")
    print(f"Confidence: {decision.confidence}")

    if is_allowed:
        execute_recovery_decision(decision)
        print("\n")
    else :
        print("Blocked by policy.\n")