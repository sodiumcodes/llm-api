from schemas import RecoveryDecision
from guardrails import apply_guardrails
from executor import execute_permitted_action
from test_scenarios import test_cases
from agent import run_recovery_agent

# Simulating events
for test_case in test_cases :
    event = test_case["event"]
    proposed_decision = test_case["proposed_decision"]
    # Apply guardrails
    proposed_decision, guardrail_result, execution_result = run_recovery_agent(
        event
    )
    print("\n========== EXECUTION RESULT ==========")
    print(execution_result)

    print("\n========== PROPOSED DECISION ==========")
    print(proposed_decision)

    print("\n========== GUARDRAIL RESULT ==========")
    print(guardrail_result)
    print("\n\n")
