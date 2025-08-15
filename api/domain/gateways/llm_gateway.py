from abc import ABC, abstractmethod
from api.domain.entities.llm_message import LLMMessage
import numpy.typing as npt

class LLMGateway(ABC):

    @abstractmethod
    def embedding(input: str) -> npt.NDArray:
        pass

    @abstractmethod
    def completions(messages: list[LLMMessage]) -> str:
        pass