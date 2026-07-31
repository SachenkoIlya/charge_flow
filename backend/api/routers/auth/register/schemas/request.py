from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    full_name: str = Field(
        description="Полное имя пользователя",
        examples=["Иван Иванов"],
    )

    email: EmailStr = Field(
        description="Адрес электронной почты пользователя",
        examples=["ivan@example.com"],
    )

    password: str = Field(
        description="Пароль пользователя",
        examples=["StrongPassword123!"],
    )

    company: str = Field(
        description="Название компании пользователя",
        examples=["ChargeFlow"],
    )

    phone: str = Field(
        description="Контактный номер телефона",
        examples=["+79991234567"],
    )

    country: str = Field(
        description="Страна регистрации пользователя",
        examples=["Россия"],
    )