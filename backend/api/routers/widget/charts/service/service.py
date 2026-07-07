from backend.api.routers.widget.charts.db import ChartsDB
from backend.api.routers.widget.charts.schemas import ChartsRequestSchema
from backend.api.routers.widget.charts.service.chart_registry import CHART_REGISTRY 
from core.base_db import Base
from core.logger.logger import logger
from backend.core.gather_named import gather_named  
import asyncio

class ChartService:
    """
    Сервисный слой для сборки и обработки аналитических графиков (компонентов дашборда).

    Использует паттерн 'Фабрика/Реестр' (Registry Pattern) для динамического 
    управления процессорами графиков. При инициализации класс кэширует экземпляры 
    всех зарегистрированных обработчиков, обеспечивая их изоляцию и переиспользование.

    Attributes:
        chart_db (ChartsDB): Слой работы с базой данных для аналитических запросов.
        handlers (dict[str, Any]): Реестр инициализированных объектов-обработчиков 
            (Handlers) для каждого типа графика.
    """
    def __init__(self, base_db: "Base"):
        """
        Инициализирует ChartService и подготавливает пул обработчиков.

        Args:
            base_db (Base): Экземпляр подключения или пула базы данных.
        """
        self.chart_db = ChartsDB(base_db)
        self.handlers = {
            name: cls(self.chart_db)
            for name, cls in CHART_REGISTRY.items()
        }

    async def resolve_charts(
        self, 
        user_id: int, 
        payload: ChartsRequestSchema
    ):
        """
        Собирает сводный аналитический экран из затребованных графиков-кубиков.

        Метод выполняет фильтрацию входящего запроса (отсекая пустые поля через 
        `exclude_none`), динамически сопоставляет графики с их обработчиками 
        из пула и запускает все SQL-выборки параллельно в виде фоновых задач (Tasks). 
        Ошибки отдельных графиков изолируются на уровне `gather_named`.

        Args:
            user_id (int): Идентификатор пользователя (инвестора) для фильтрации данных.
            payload (ChartsRequestSchema): Валидированная Pydantic-схема запроса, 
                содержащая параметры для каждого запрашиваемого виджета.

        Returns:
            dict: Словарь с корневым ключом 'charts', внутри которого лежат 
                готовые структуры данных для фронтенда, сгруппированные по именам графиков.
        """
        init_cls_charts = {}

        for name, value in payload.model_dump(exclude_none=True).items():
            handler = self.handlers.get(name)  

            if handler is None:
                logger.warning(f"Обработчик для графика '{name}' не найден в реестре!")
                continue
            
            init_cls_charts[name] = asyncio.create_task(
                handler.build(user_id, value)
            )

        data = await gather_named(init_cls_charts)
        return {'charts': data}

