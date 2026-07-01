
from pydantic import BaseModel, Field


class RegisterUserResponse(BaseModel):
    """
    Ответ после регистрации пользователя.
    """
    user_id: int = Field(
        description='user id',
        examples=[1]
    ),
    detail: str = Field(
        description="Сообщение о результате операции.",
        examples=["Пользователь зарегестрирован"],
    )