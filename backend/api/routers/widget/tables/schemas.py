from pydantic import BaseModel, Field

from backend.api.routers.widget.tables.station_raiting.schemas import StationRatingParam




class TablesRequestSchema(BaseModel):
    """Схема входящих данных для пакетного запроса табличных метрик панели управления.
    
    Позволяет гибко запрашивать аналитические таблицы и рейтинги (например, 
    рейтинг эффективности станций) в рамках единого HTTP-запроса к API.
    """
    station_rating: StationRatingParam | None = Field(
        default=None,
        description="Параметры фильтрации для построения рейтинга станций. Если null — таблица рейтинга не рассчитывается."
    )