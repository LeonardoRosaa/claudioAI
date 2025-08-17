from pydantic import BaseModel, Field

from api.domain.entities.completion_message import CompletionMessage


class CreateCompletion(BaseModel):
    help_desk_id: int = Field(examples=[123])
    project_name: str = Field(max_length=20, examples=["tesla_motors"])
    messages: list[CompletionMessage]
