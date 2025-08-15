from abc import ABC, abstractmethod
import numpy.typing as npt
from api.domain.entities.vector_search_result import VectorSearchResult

class VectorGateway(ABC):

    @abstractmethod
    def filter(project_name: str, vector: npt.NDArray) -> list[VectorSearchResult]:
        pass