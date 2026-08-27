from pydantic import BaseModel, Field, model_validator
from typing import Literal

#What the LLM wants to do.
class RecoveryDecision(BaseModel):
    action: Literal["retry", "notify", "escalate", "stop"]
    retry_after_minutes: int | None = Field(
        default=None,
        ge=1
    )
    reason: str = Field(
        min_length=1,
        description="A concise explanation for the chosen recovery action."
    )
    confidence: float = Field(
        ge=0,
        le=1
    )
    @model_validator(mode="after")
    def validate_retry_rules(self):

        if self.action == "retry" and self.retry_after_minutes is None:
            raise ValueError(
                "retry_after_minutes is required when action is 'retry'"
            )

        if self.action != "retry" and self.retry_after_minutes is not None:
            raise ValueError(
                "retry_after_minutes must be None unless action is 'retry'"
            )

        return self
    
class ExecutionResult(BaseModel):
    action: Literal[
        "retry",
        "notify",
        "escalate",
        "stop"
    ]

    executed: bool

    status: Literal[
        "executed",
        "blocked",
        "pending_review"
    ]

    message: str
    
#What the system finally allows.
class GuardrailResult(BaseModel):
    original_action: Literal[
        "retry",
        "notify",
        "escalate",
        "stop"
    ]

    final_action: Literal[
        "retry",
        "notify",
        "escalate",
        "stop"
    ]

    require_human_review: bool

    violations: list[str]
    warnings : list[str]