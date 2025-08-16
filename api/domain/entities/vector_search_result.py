import numpy
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class VectorSearchResultType(Enum):
    N1 = "N1"
    N2 = "N2"


class VectorSearchResult(BaseModel):
    score: float = Field(alias="@search.score", serialization_alias="score")
    content: str
    type: VectorSearchResultType
