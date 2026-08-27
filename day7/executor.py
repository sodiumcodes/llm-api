from schemas import GuardrailResult, ExecutionResult
def execute_permitted_action(
    result: GuardrailResult
) -> ExecutionResult:

    # =================================
    # 1. BLOCKED
    # =================================

    if result.final_action == "stop":
        return ExecutionResult(
            action="stop",
            executed=False,
            status="blocked",
            message="Execution blocked: autonomous recovery stopped."
        )

    # =================================
    # 2. HUMAN REVIEW
    # =================================

    if result.require_human_review:
        return ExecutionResult(
            action=result.final_action,
            executed=False,
            status="pending_review",
            message=(
                f"Execution paused: "
                f"'{result.final_action}' requires human review."
            )
        )

    # =================================
    # 3. EXECUTION
    # =================================

    if result.final_action == "escalate":
        return ExecutionResult(
            action="escalate",
            executed=True,
            status="executed",
            message="Escalation executed successfully."
        )

    elif result.final_action == "retry":
        return ExecutionResult(
            action="retry",
            executed=True,
            status="executed",
            message="Retry executed successfully."
        )

    elif result.final_action == "notify":
        return ExecutionResult(
            action="notify",
            executed=True,
            status="executed",
            message="Notification sent successfully."
        )

    # =================================
    # FALLBACK
    # =================================

    return ExecutionResult(
        action="stop",
        executed=False,
        status="blocked",
        message="Unknown action. Execution blocked."
    )