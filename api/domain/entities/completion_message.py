from api.domain.entities.completion_role import CompletionRole
from pydantic import BaseModel, Field


class CompletionMessage(BaseModel):
    role: CompletionRole = Field(examples=["USER"])
    content: str = Field(max_length=200, examples=["What is Tesla?"])
