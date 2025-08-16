from api.domain.entities.llm_message_role import LLMMessageRole


class LLMMessage:

    def __init__(self, role: LLMMessageRole, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role.value, "content": self.content}
