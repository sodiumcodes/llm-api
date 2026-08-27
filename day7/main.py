from test_cases import test_cases
from agent import run_recovery_agent


tp = fp = tn = fn = 0
decision_pass = 0
decision_fail = 0


for i, test_case in enumerate(test_cases, start=1):

    event = test_case["event"]

    proposed_decision, guardrail_result, execution_result = (
        run_recovery_agent(event)
    )

    # LLM's prediction
    action = proposed_decision.action

    # Expected decision
    expected_action = test_case["expected_action"]

    # Ground truth for classification
    actual_outcome = test_case["actual_outcome"]


    print("\n========== DEBUG ==========")

    print(f"Iteration: {i}")
    print(f"Case: {test_case['name']}")

    print(f"Expected Action: {expected_action}")
    print(f"Agent Proposed Action: {action}")

    print(f"Final Execution Action: {execution_result.action}")

    print(f"Actual Outcome: {actual_outcome}")


    # ==========================================
    # DECISION ACCURACY
    # ==========================================

    if action == expected_action:
        decision_pass += 1
        print("Decision Test: PASS")

    else:
        decision_fail += 1
        print("Decision Test: FAIL")


    # ==========================================
    # CLASSIFICATION METRICS
    #
    # Positive prediction = escalate
    # Actual positive = needed_escalation
    # ==========================================

    if (
        action == "escalate"
        and actual_outcome == "needed_escalation"
    ):
        tp += 1
        label = "TP"


    elif (
        action == "escalate"
        and actual_outcome == "self_resolved"
    ):
        fp += 1
        label = "FP"


    elif (
        action != "escalate"
        and actual_outcome == "needed_escalation"
    ):
        fn += 1
        label = "FN"


    elif (
        action != "escalate"
        and actual_outcome == "self_resolved"
    ):
        tn += 1
        label = "TN"


    print(f"Classification: {label}")


# ==========================================
# METRICS
# ==========================================

precision = (
    tp / (tp + fp)
    if (tp + fp) > 0
    else 0
)

recall = (
    tp / (tp + fn)
    if (tp + fn) > 0
    else 0
)

f1_score = (
    2 * precision * recall / (precision + recall)
    if (precision + recall) > 0
    else 0
)


print("\n========== EVALUATION REPORT ==========")

print(f"True Positives: {tp}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Negatives: {tn}")

print(f"\nDecision Passes: {decision_pass}")
print(f"Decision Failures: {decision_fail}")

print(f"\nPrecision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1_score:.2f}")