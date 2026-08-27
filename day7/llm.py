import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from schemas import RecoveryDecision


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def get_recovery_decision(
    event: dict
) -> RecoveryDecision:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": """
                        You are a payment recovery decision agent.

                        Analyze the payment failure event and propose exactly one action.

                        Possible actions:
                        - retry
                        - notify
                        - escalate
                        - stop

                        Use the following decision framework:

                        1. RETRY
                        Choose "retry" only when the failure appears temporary and another
                        payment attempt may reasonably succeed.

                        Examples:
                        - network_timeout
                        - temporary_bank_error

                        2. ESCALATE
                        Choose "escalate" when the payment requires investigation or human
                        intervention.

                        Escalate when one or more of the following applies:
                        - failure_type is "persistent_failure"
                        - the payment has repeatedly failed
                        - retry_count is high or the retry limit has been exceeded
                        - the transaction amount is high and the failure is serious
                        - the situation cannot be safely resolved automatically

                        Important:
                        Repeated persistent failures should normally be escalated for
                        investigation rather than stopped.

                        3. STOP
                        Choose "stop" only when further recovery is clearly impossible or
                        unsafe.

                        Examples:
                        - invalid_account
                        - account_closed
                        - invalid_payment_method

                        Do NOT treat "persistent_failure" by itself as a reason to stop.
                        Persistent failures require investigation and should normally be
                        escalated.

                        4. NOTIFY
                        Choose "notify" when the main required action is to inform the
                        customer and investigation or retry is not required.

                        Return a JSON object with exactly these fields:

                        {
                            "action": "retry | notify | escalate | stop",
                            "retry_after_minutes": integer or null,
                            "reason": "concise explanation",
                            "confidence": number between 0 and 1
                        }

                        You are only proposing an action.
                        You do not have permission to override system guardrails.
                    """
            },
            {
                "role": "user",
                "content": json.dumps(event)
            }
        ]
    )

    content = response.choices[0].message.content
    # Remove whitespace
    content = content.strip()

    # Remove Markdown JSON fences if present
    if content.startswith("```json"):
        content = content.removeprefix("```json").removesuffix("```").strip()

    elif content.startswith("```"):
        content = content.removeprefix("```").removesuffix("```").strip()

    try:
        decision_data = json.loads(content)

    except json.JSONDecodeError:
        print("\n========== INVALID LLM RESPONSE ==========")
        print("The model did not return valid JSON.")

        raise ValueError(
            f"Invalid JSON received from LLM: {content}"
        )

    return RecoveryDecision(
        **decision_data
    )