
#! FLOW OF apply_guardrails()

# Can I trust the input?
#         ↓
# Is there a condition that blocks autonomous execution?
#         ↓
# If not, does this decision need human review?
#         ↓
# Return the permitted result

from schemas import RecoveryDecision, GuardrailResult

MAX_RETRIES = 3
PERMANENT_FAILURES = {
    "invalid_account",
    "account_closed",
    "invalid_payment_method"
}
LOW_CONFIDENCE_THRESHOLD = 0.6
HIGH_VALUE_THRESHOLD = 50000

MAX_TOTAL_FAILURES = 5

REQUIRED_EVENT_FIELDS = {
    "retry_count",
    "failure_type",
    "amount",
    "total_failures"
}

#? -> GaurdrailResult is return type annotation
def apply_guardrails(
    proposed_decision: RecoveryDecision,
    event: dict
) -> GuardrailResult:

    # Start by assuming the LLM's action is allowed
    final_action = proposed_decision.action

    # Store any rules that were violated and any warnings
    violations: list[str] = []
    warnings: list[str] = []

    # By default, human review is not required
    require_human_review = False

    # =================================
    # RULE 7: INPUT VALIDATION
    # =================================
    missing_fields = REQUIRED_EVENT_FIELDS - event.keys()
    if missing_fields:
        final_action = "stop"
        violations.append(
            f"Missing required event fields: {', '.join(sorted(missing_fields))}"
        )

# TERMINAL GUARDRAILS

    # -----------------------------
    # RULE 1: Maximum retry limit
    # -----------------------------
    elif (
        proposed_decision.action == "retry"
        and event["retry_count"] >= MAX_RETRIES
    ):
        final_action = "stop"

        violations.append(
            "Maximum retry limit reached"
        )

    # -----------------------------
    # RULE 2: Permanent failures
    # cannot be retried
    # -----------------------------

    elif (
        proposed_decision.action == "retry"
        and event["failure_type"] in PERMANENT_FAILURES
    ):
        final_action = "stop"

        violations.append(
            "Permanent failure cannot be retried"
        )

    # *RULE 5: Retry requires delay : taken care in the RecoveryDecision model

    # -----------------------------
    # RULE 6: Too many total failures
    # -----------------------------
    elif event["total_failures"] >= MAX_TOTAL_FAILURES:

        final_action = "stop"
        require_human_review = True
        violations.append(
            "Maximum total failure limit reached"
        )
    # =================================
    # NON-TERMINAL GUARDRAILS
    # =================================

    else:
        # Rule: Low confidence
        if proposed_decision.confidence < LOW_CONFIDENCE_THRESHOLD :
            require_human_review = True
            warnings.append(
                "Low confidence: human review required"
            )
        # -----------------------------
        # RULE 4: High-value transaction
        # -----------------------------
        if event["amount"] >= HIGH_VALUE_THRESHOLD:
            require_human_review = True
            warnings.append(
                "High-value transaction: human review required"
            ) 
        # -----------------------------
        # RULE 8: Escalation requires
        # human review
        # -----------------------------

        if proposed_decision.action == "escalate":
            require_human_review = True
            warnings.append(
                "Escalation requires human review"
            )
    return GuardrailResult(
        original_action=proposed_decision.action,
        final_action=final_action,
        require_human_review=require_human_review,
        violations=violations,
        warnings=warnings
    )
