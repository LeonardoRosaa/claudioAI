from fastapi import APIRouter, Depends
from api.domain.entities.create_completion import CreateCompletion
from api.domain.services.conversation_service import ConversationService
from api.domain.entities.completion_response import CompletionResponse

router = APIRouter()


@router.post(
    "/completions", tags=["create", "completions"], response_model=CompletionResponse
)
async def create(
    completion: CreateCompletion,
    conversation_service: ConversationService = Depends(ConversationService),
):
    return conversation_service.completion(completion=completion)
