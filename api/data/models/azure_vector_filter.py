import numpy.typing as npt

class AzureVectorFilter():
    def __init__(self, project_name: str, vector: npt.NDArray):
        self.project_name = project_name
        self.vector = vector

    def to_dict(self):
        return {
            "count": True,
            "select": "content, type",
            "top": 10,
            "filter": f"projectName eq '{self.project_name}'",
            "vectorQueries": [
                {
                    "vector": self.vector.tolist(),
                    "k": 5,
                    "fields": "embeddings",
                    "kind": "vector"
                }
            ]
        }