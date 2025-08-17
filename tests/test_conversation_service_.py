from api.domain.entities.create_completion import CreateCompletion
from api.domain.entities.completion_role import CompletionRole
from api.domain.entities.completion_message import CompletionMessage
from api.domain.entities.completion_response import CompletionResponse
from api.domain.entities.vector_search_result import (
    VectorSearchResult,
    VectorSearchResultType,
)
from api.domain.services.conversation_service import ConversationService
import pytest
from unittest.mock import Mock


class TestConversationService:

    @pytest.fixture
    def mock_llm_gateway(self):
        mock_llm = Mock()
        mock_llm.embedding.return_value = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_llm.completions.return_value = "This is a response from the AI assistant."
        return mock_llm

    @pytest.fixture
    def mock_vector_gateway(self):
        mock_vector = Mock()
        mock_vector.filter.return_value = [
            VectorSearchResult(
                content="Sample documentation content",
                **{"@search.score": 0.75},
                type=VectorSearchResultType.N1,
            )
        ]
        return mock_vector

    @pytest.fixture
    def conversation_service(self, mock_llm_gateway, mock_vector_gateway):
        return ConversationService(llm=mock_llm_gateway, vector=mock_vector_gateway)

    @pytest.fixture
    def sample_completion_request(self):
        return CreateCompletion(
            help_desk_id=1234,
            project_name="test_project",
            messages=[
                CompletionMessage(role=CompletionRole.USER, content="What is Tesla?"),
                CompletionMessage(
                    role=CompletionRole.AGENT,
                    content="What car models does Tesla offer?",
                ),
                CompletionMessage(
                    role=CompletionRole.USER, content="Can I charge a Tesla at home?"
                ),
            ],
        )

    def test_completion_success_with_user_messages(
        self, conversation_service, sample_completion_request
    ):
        result = conversation_service.completion(sample_completion_request)

        assert isinstance(result, CompletionResponse)
        assert len(result.messages) == 4
        assert len(result.sections_retrived) == 2
        assert result.handover_to_human_need is False

        user_messages = [
            msg for msg in result.messages if msg.role == CompletionRole.USER
        ]
        assert len(user_messages) == 2

        agent_messages = [
            msg for msg in result.messages if msg.role == CompletionRole.AGENT
        ]
        assert len(agent_messages) == 2
        
    def test_completion_success_for_no_enough_context(
        self, conversation_service, sample_completion_request, mock_vector_gateway
    ):
        mock_vector_gateway.filter.return_value = [
            VectorSearchResult(
                content="Sample documentation content",
                **{"@search.score": 0.4},
                type=VectorSearchResultType.N1,
            )
        ]
        
        result = conversation_service.completion(sample_completion_request)

        assert isinstance(result, CompletionResponse)
        assert len(result.messages) == 4
        assert len(result.sections_retrived) == 2
        assert result.handover_to_human_need is True

        user_messages = [
            msg for msg in result.messages if msg.role == CompletionRole.USER
        ]
        assert len(user_messages) == 2

        agent_messages = [
            msg for msg in result.messages if msg.role == CompletionRole.AGENT
        ]
        assert len(agent_messages) == 2

    def test_completion_handover_to_human_needed(
        self, conversation_service, mock_vector_gateway
    ):
        mock_vector_gateway.filter.return_value = [
            VectorSearchResult(
                content="Sample documentation content",
                **{"@search.score": 0.75},
                type=VectorSearchResultType.N2,
            )
        ]

        completion_request = CreateCompletion(
            help_desk_id=123,
            project_name="test_project",
            messages=[
                CompletionMessage(role=CompletionRole.USER, content="Complex issue")
            ],
        )

        result = conversation_service.completion(completion_request)

        assert result.handover_to_human_need is True
