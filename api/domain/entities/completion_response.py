from api.domain.entities.completion_message import CompletionMessage
from api.domain.entities.vector_search_result import VectorSearchResult
from pydantic import BaseModel

class CompletionResponse(BaseModel):
    messages: list[CompletionMessage]
    sections_retrived: list[VectorSearchResult]
    handover_to_human_need: bool