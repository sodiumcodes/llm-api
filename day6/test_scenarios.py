from schemas import RecoveryDecision
from guardrails import apply_guardrails
from executor import execute_permitted_action


test_cases = [

    # ============================================================
    # TEST CASE 1: Safe Retry
    # ============================================================
    {
        "name": "Safe Retry",

        "event": {
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="The failure appears temporary.",
            confidence=0.9
        )
    }
]
