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

                    Rules for your proposal:

                    - Choose retry only when another attempt may reasonably succeed.
                    - Choose stop for failures that appear permanent.
                    - Choose escalate when the situation requires investigation.
                    - Choose notify when the customer should be informed.

                    Return a JSON object with exactly these fields:

                    {
                        "action": "retry | notify | escalate | stop",
                        "retry_after_minutes": integer or null,
                        "reason": "concise explanation",
                        "confidence": number between 0 and 1
                    }

                    Important:
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

    print("\n========== RAW LLM RESPONSE ==========")
    print(content)
    if content.startswith("```json") : 
        content = content.removeprefix("```json").removesuffix("```").strip()
    decision_data = json.loads(content)

    return RecoveryDecision(
        **decision_data
    )