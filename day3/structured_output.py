from pydantic import BaseModel , Field, model_validator
from typing import Literal
import json
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

decision = RecoveryDecision(
    action="retry",
    reason="The failure appears temporary and the customer has sufficient retry attempts remaining.",
    retry_after_minutes=30,
    confidence=0.91
)
d= RecoveryDecision (
    action="notify",
    reason="Temporary failure detected",
    retry_after_minutes=None,
    confidence=0.9
)


decision_schema = RecoveryDecision.model_json_schema()

        
        

    