test_cases = [
    # ==========================================
    # FP-ORIENTED CASES
    # Ground truth: escalation was NOT needed.
    # If agent predicts "escalate" -> FP
    # ==========================================

    {
        "name": "FP Case 1 - High Value Temporary Timeout",

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


    {
        "name": "FP Case 2 - High Value Temporary Bank Error",

        "event": {
            "payment_id": "pay_fp_002",
            "retry_count": 1,
            "failure_type": "temporary_bank_error",
            "amount": 300000,
            "total_failures": 1
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    {
        "name": "FP Case 3 - Repeated Network Timeout",

        "event": {
            "payment_id": "pay_fp_003",
            "retry_count": 2,
            "failure_type": "network_timeout",
            "amount": 100000,
            "total_failures": 2
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    {
        "name": "FP Case 4 - Temporary Error With High Amount",

        "event": {
            "payment_id": "pay_fp_004",
            "retry_count": 2,
            "failure_type": "temporary_bank_error",
            "amount": 500000,
            "total_failures": 2
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    {
        "name": "FP Case 5 - Medium Repeated Timeout",

        "event": {
            "payment_id": "pay_fp_005",
            "retry_count": 2,
            "failure_type": "network_timeout",
            "amount": 75000,
            "total_failures": 3
        },

        "expected_action": "retry",

        "actual_outcome": "self_resolved"
    },


    # ==========================================
    # FN-ORIENTED CASES
    # Ground truth: escalation WAS needed.
    # If agent predicts anything except
    # "escalate" -> FN
    # ==========================================

    {
        "name": "FN Case 1 - Low Value Persistent Failure",

        "event": {
            "payment_id": "pay_fn_001",
            "retry_count": 3,
            "failure_type": "persistent_failure",
            "amount": 5000,
            "total_failures": 3
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    },


    {
        "name": "FN Case 2 - Persistent Failure After Few Attempts",

        "event": {
            "payment_id": "pay_fn_002",
            "retry_count": 2,
            "failure_type": "persistent_failure",
            "amount": 10000,
            "total_failures": 2
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    },


    {
        "name": "FN Case 3 - Unknown High Value Failure",

        "event": {
            "payment_id": "pay_fn_003",
            "retry_count": 3,
            "failure_type": "unknown_failure",
            "amount": 250000,
            "total_failures": 3
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    },


    {
        "name": "FN Case 4 - Repeated Unknown Failure",

        "event": {
            "payment_id": "pay_fn_004",
            "retry_count": 4,
            "failure_type": "unknown_failure",
            "amount": 30000,
            "total_failures": 4
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    },


    {
        "name": "FN Case 5 - Medium Value Persistent Failure",

        "event": {
            "payment_id": "pay_fn_005",
            "retry_count": 3,
            "failure_type": "persistent_failure",
            "amount": 25000,
            "total_failures": 3
        },

        "expected_action": "escalate",

        "actual_outcome": "needed_escalation"
    }
]