import requests
import numpy.typing as npt
import json

from api.config import settings
from api.domain.gateways.vector_gateway import VectorGateway
from api.domain.entities.vector_search_result import VectorSearchResult
from api.data.models.azure_vector_filter import AzureVectorFilter


class AzureVectorGateway(VectorGateway):

    def filter(
        self, project_name: str, vector: npt.NDArray
    ) -> list[VectorSearchResult]:
        headers = {
            "Content-Type": "application/json",
            "api-key": settings.VECTOR_DB_KEY,
        }
        filter = AzureVectorFilter(project_name, vector)

        response = requests.post(
            settings.AZURE_URL, json=filter.to_dict(), headers=headers
        )

        return [VectorSearchResult.model_validate(i) for i in response.json()["value"]]
