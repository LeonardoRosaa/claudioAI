import numpy

from api.domain.gateways.llm_gateway import LLMGateway
from openai import OpenAI
from api.config import settings
from api.domain.entities.llm_message import LLMMessage


class OpenAILLMGateway(LLMGateway):
    def __init__(self):
        self.openai = OpenAI(api_key=settings.OPENAI_KEY)

    def embedding(self, input: str):
        response = self.openai.embeddings.create(
            model="text-embedding-3-large", input=input
        )

        return numpy.array(response.data[0].embedding)

    def completions(self, messages: list[LLMMessage]) -> str:
        response = self.openai.chat.completions.create(
            model="gpt-4o", messages=[ob.to_dict() for ob in messages]
        )

        return response.choices[0].message.content.strip()
