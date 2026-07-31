from pydantic import BaseModel, Field


class UserCreateResponse(BaseModel):
    """
    Ответ после регистрации пользователя.
    """
    user_id: int = Field(
        description="Уникальный идентификатор зарегистрированного пользователя.",
        examples=[1],
    )
    detail: str = Field(
        description="Сообщение о результате выполнения операции.",
        examples=["Пользователь успешно зарегистрирован."],
    )