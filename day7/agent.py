from schemas import (
    RecoveryDecision,
    GuardrailResult,
    ExecutionResult
)

from llm import get_recovery_decision
from guardrails import apply_guardrails
from executor import execute_permitted_action


def run_recovery_agent(
    event: dict
) -> tuple[
    RecoveryDecision,
    GuardrailResult,
    ExecutionResult
]:

    # =================================
    # STEP 1: LLM PROPOSES A DECISION
    # =================================

    proposed_decision = get_recovery_decision(
        event
    )

    # =================================
    # STEP 2: GUARDRAILS DECIDE
    # WHAT IS PERMITTED
    # =================================

    guardrail_result = apply_guardrails(
        proposed_decision,
        event
    )

    # =================================
    # STEP 3: EXECUTOR PERFORMS
    # ONLY THE PERMITTED ACTION
    # =================================

    execution_result = execute_permitted_action(
        guardrail_result
    )

    return (
        proposed_decision,
        guardrail_result,
        execution_result
    )