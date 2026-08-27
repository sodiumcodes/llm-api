from schemas import RecoveryDecision
test_cases = [

    # ==========================================
    # TN / Possible FP depending on agent decision
    # ==========================================
    {
        "name": "High Value Temporary Timeout",

        "event": {
            "payment_id": "pay_fp_001",
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 200000,
            "total_failures": 1
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    # ==========================================
    # TN / Possible FP depending on agent decision
    # ==========================================
    {
        "name": "Temporary Error That Self Resolved",

        "event": {
            "payment_id": "pay_009",
            "retry_count": 2,
            "failure_type": "temporary_bank_error",
            "amount": 20000,
            "total_failures": 2
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    # ==========================================
    # GUARANTEED FP
    # Agent predicts: escalate
    # Actual outcome: self_resolved
    # ==========================================
    {
        "name": "FP - Agent Escalates But Escalation Was Not Needed",

        "event": {
            "payment_id": "pay_fp_002",
            "retry_count": 1,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 1
        },

        "proposed_decision": RecoveryDecision(
            action="escalate",
            retry_after_minutes=None,
            reason="Forced escalation for evaluation.",
            confidence=0.90
        ),

        "actual_outcome": "self_resolved"
    },


    # ==========================================
    # GUARANTEED FN
    # Agent predicts: stop
    # Actual outcome: needed_escalation
    # ==========================================
    {
        "name": "FN - Agent Does Not Escalate But Escalation Was Needed",

        "event": {
            "payment_id": "pay_fn_001",
            "retry_count": 5,
            "failure_type": "persistent_failure",
            "amount": 100000,
            "total_failures": 4
        },

        "proposed_decision": RecoveryDecision(
            action="stop",
            retry_after_minutes=None,
            reason="Forced non-escalation for evaluation.",
            confidence=0.90
        ),

        "actual_outcome": "needed_escalation"
    },


    # ==========================================
    # TP / Possible FN depending on agent decision
    # ==========================================
    {
        "name": "Repeated Failure Requires Investigation",

        "event": {
            "payment_id": "pay_010",
            "retry_count": 5,
            "failure_type": "persistent_failure",
            "amount": 80000,
            "total_failures": 4
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    },


    # ==========================================
    # TN
    # ==========================================
    {
        "name": "Single Temporary Failure",

        "event": {
            "payment_id": "pay_011",
            "retry_count": 0,
            "failure_type": "network_timeout",
            "amount": 10000,
            "total_failures": 1
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    }
]