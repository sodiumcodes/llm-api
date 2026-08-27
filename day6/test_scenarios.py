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
    },

    # ============================================================
    # TEST CASE 2: Maximum Retry Limit
    # ============================================================
    {
        "name": "Maximum Retry Limit",

        "event": {
            "retry_count": 3,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 3
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="Trying recovery again.",
            confidence=0.9
        )
    },

    # ============================================================
    # TEST CASE 3: Permanent Failure
    # ============================================================
    {
        "name": "Permanent Failure",

        "event": {
            "retry_count": 1,
            "failure_type": "invalid_account",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="Attempting recovery.",
            confidence=0.9
        )
    },

    # ============================================================
    # TEST CASE 4: Low Confidence
    # ============================================================
    {
        "name": "Low Confidence",

        "event": {
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="The failure might be temporary.",
            confidence=0.4
        )
    },

    # ============================================================
    # TEST CASE 5: High-Value Transaction
    # ============================================================
    {
        "name": "High-Value Transaction",

        "event": {
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 100000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="The failure appears temporary.",
            confidence=0.9
        )
    },

    # ============================================================
    # TEST CASE 6: Escalation
    # ============================================================
    {
        "name": "Escalation",

        "event": {
            "retry_count": 1,
            "failure_type": "unknown_error",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="escalate",
            retry_after_minutes=None,
            reason="The failure requires further investigation.",
            confidence=0.9
        )
    },

    # ============================================================
    # TEST CASE 7: Maximum Total Failures
    # ============================================================
    {
        "name": "Maximum Total Failures",

        "event": {
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 5
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="Attempting another recovery.",
            confidence=0.9
        )
    },

    # ============================================================
    # TEST CASE 8: Missing Required Event Field
    # ============================================================
    {
        "name": "Missing Required Event Field",

        "event": {
            "retry_count": 1,
            "failure_type": "missing_payment_id",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="retry",
            retry_after_minutes=30,
            reason="Attempting recovery.",
            confidence=0.9
        )
    }
]

