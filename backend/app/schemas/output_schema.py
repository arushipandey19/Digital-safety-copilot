from pydantic import BaseModel
from typing import List


class Entities(BaseModel):
    phone_numbers: List[str]
    emails: List[str]


class AnalysisOutput(BaseModel):
    input_type: str
    text: str
    urls: List[str]
    claimed_organization: str
    entities: Entities