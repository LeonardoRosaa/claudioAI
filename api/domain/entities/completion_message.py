from api.domain.entities.completion_role import CompletionRole
from pydantic import BaseModel

class CompletionMessage(BaseModel):
    role: CompletionRole
    content: str