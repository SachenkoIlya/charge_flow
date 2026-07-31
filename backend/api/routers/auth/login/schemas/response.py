from pydantic import BaseModel, Field

class OperatorConnectResponse(BaseModel):
    """
    Ответ после успешного подключения оператора.
    """
    detail: str = Field(
        description="Сообщение о результате операции.",
        examples=["Оператор подключен"],
    )