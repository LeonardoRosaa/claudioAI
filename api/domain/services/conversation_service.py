from api.domain.gateways.llm_gateway import LLMGateway
from api.domain.gateways.vector_gateway import VectorGateway
from api.data.gateways.azure_vector_gateway import AzureVectorGateway
from api.data.gateways.openai_llm_gateway import OpenAILLMGateway
from api.domain.entities.create_completion import CreateCompletion
from api.domain.entities.llm_message import LLMMessage
from api.domain.entities.llm_message_role import LLMMessageRole
from api.domain.entities.completion_role import CompletionRole
from api.domain.entities.completion_message import CompletionMessage
from api.domain.entities.completion_response import CompletionResponse
from api.domain.entities.vector_search_result import VectorSearchResult, VectorSearchResultType
from fastapi import Depends
from api.infrastructure.logger import logger

import concurrent.futures

class ConversationService():

    def __init__(self, llm: LLMGateway = Depends(OpenAILLMGateway), vector: VectorGateway = Depends(AzureVectorGateway)):
        self.llm = llm
        self.vector = vector

    def completion(self, completion: CreateCompletion):
        logger.info(f"Starting completion to {completion.help_desk_id}")
        contents = [i for i in completion.messages if i.role == CompletionRole.USER]
        messages: list[CompletionMessage] = []
        sections_retrived: list[VectorSearchResult] = [] 
        handover_to_human_needed = False

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for _, response in zip(contents, executor.map(lambda x: self._build_completion(completion.project_name, x), contents)):
                messages += response[0]
                sections_retrived += response[1]
                handover_to_human_needed = True if handover_to_human_needed else response[2]
        
        if handover_to_human_needed:
            logger.info(f"A human should check {completion.help_desk_id}")

        return CompletionResponse(
            messages=messages,
            sections_retrived=sections_retrived,
            handover_to_human_need=handover_to_human_needed
        )
    
    def _build_completion(self, project_name: str, content: CompletionMessage):
        embedding = self.llm.embedding(content.content)

        sections_retrived = self.vector.filter(project_name, embedding)
        contexts = self._clarify(sections_retrived)
        is_empty = len(contexts) == 0

        if is_empty:
            logger.info(f"No enough context to \"{content.content}\"")
            return ([], sections_retrived, True)
        
        system_requirements = [LLMMessage(role=LLMMessageRole.SYSTEM, content=i.content) for i in contexts] + [LLMMessage(role=LLMMessageRole.USER, content=content.content,),]
        system_response = self.llm.completions(system_requirements)
        messages = [content, CompletionMessage(role=CompletionRole.AGENT, content=system_response)]
        
        return (messages, sections_retrived, self._need_human(contexts))
    
    """
     Remove items with a score less than 0.50
    """
    def _clarify(self, contexts: list[VectorSearchResult]) -> list[VectorSearchResult]:    
        return [context for context in contexts if context.score >= 0.50]
    
    def _need_human(self, contexts: list[VectorSearchResult]) -> bool:
        return any(context for context in contexts if context.type == VectorSearchResultType.N2)
        