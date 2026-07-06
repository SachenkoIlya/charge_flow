from pydantic import BaseModel, Field


class CompanySchema(BaseModel):
    id: int = Field(
        description='Уникальный идентификатор компании в системе',
        examples=[1]
    )
    name: str = Field(
        description='Официальное или торговое наименование компании инвестора',
        examples=['ООО ИнвестКапитал']
    )