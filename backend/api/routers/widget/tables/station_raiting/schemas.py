from pydantic import BaseModel, Field


class StationRatingParam(BaseModel):
    """Параметры фильтрации для построения рейтинга станций.
    
    Задает временные рамки, за которые будет производиться расчет и 
    сортировка станций (например, по выручке, утилизации или объему энергии).
    """
    date_from: str = Field(
        description="Начальная дата расчетного периода (включительно) в формате YYYY-MM-DD",
        examples=["2026-06-01"]
    )
    date_to: str = Field(
        description="Конечная дата расчетного периода (включительно) в формате YYYY-MM-DD",
        examples=["2026-06-30"]
    )