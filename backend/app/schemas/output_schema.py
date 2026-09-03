from pydantic import BaseModel, Field
from typing import List


class Entities(BaseModel):
    phone_numbers: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)


class AnalysisOutput(BaseModel):
    input_type: str = ""
    text: str = ""
    urls: List[str] = Field(default_factory=list)
    claimed_organization: str = ""
    entities: Entities = Field(default_factory=Entities)

    risk_level: str = "UNKNOWN"
    explanation: str = ""
    safe_actions: List[str] = Field(default_factory=list)
    evidence_chain: List[dict] = Field(default_factory=list)