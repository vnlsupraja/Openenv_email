# env/models.py
from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: str
    subject: str
    body: str
    sender: str
    priority: Optional[str] = None
    category: Optional[str] = None

class Observation(BaseModel):
    inbox: List[Email]
    last_action_result: Optional[str]

class Action(BaseModel):
    type: str  # classify, prioritize, reply, archive, escalate
    email_id: str
    content: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str