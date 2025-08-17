import numpy
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class VectorSearchResultType(Enum):
    N1 = "N1"
    N2 = "N2"


class VectorSearchResult(BaseModel):
    score: float = Field(
        alias="@search.score", serialization_alias="score", examples=[0.899]
    )
    content: str = Field(
        examples=[
            "Tesla is a technology and automotive company focused on producing electric vehicles, energy solutions, and autonomous driving technology."
        ]
    )
    type: VectorSearchResultType = Field(examples=["N1"])
