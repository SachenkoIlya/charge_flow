from pydantic import BaseModel


class CompanySchema(BaseModel):
    id: int
    name: str