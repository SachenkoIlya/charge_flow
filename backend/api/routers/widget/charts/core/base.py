from abc import ABC
from backend.core.gather_named import gather_named
from core.base_db import Base
from pydantic import BaseModel
from core.logger.logger import logger
import asyncio  


class BaseService(ABC):
    """Абстрактный базовый класс для сервисного слоя приложения.

    Использует паттерн реестра для динамической инициализации зависимых
    обработчиков (handlers). Каждый дочерний класс определяет свой тип (`mode`)
    и набор доступных процессоров через `registry`.

    Attributes:
        registry (dict): Словарь классов-обработчиков, где ключ — имя,
            а значение — класс обработчика.
        mode (str): Уникальный строковый идентификатор типа сервиса.
        db (Any): Экземпляр слоя работы с базой данных (или специализированная обертка).
        handlers (dict): Словарь инициализированных объектов-обработчиков,
            получивших доступ к `db`.
    """
    registry:dict = {}
    mode: str = ''
    
    def __init__(self, base_db: "Base"):
        """Инициализирует базу данных и регистрирует все связанные обработчики.
        Args:
            base_db (Base): Объект подключения к БД или специализированный слой данных.
        """
        self.db = base_db
        self.handlers = {
            name: cls(self.db)
            for name, cls 
            in self.registry.items()
        }
    
    async def _execute(
        self, 
        user_id: int, 
        payload: BaseModel
    ):
        """Внутренний метод для параллельной сборки графиков через реестр обработчиков.

        Итерируется по переданным параметрам запроса, сопоставляет их с доступными 
        в реестре обработчиками, упаковывает вызовы в `asyncio.create_task` для 
        параллельного выполнения и собирает результаты. Если обработчик не найден, 
        логирует предупреждение и пропускает его.

        Args:
            user_id (int): Идентификатор пользователя для фильтрации данных графиков.
            payload (BaseModel): Pydantic-модель с входными данными. Названия полей 
                должны совпадать с ключами обработчиков в `self.handlers`.

        Returns:
            dict: Словарь с ключом из `self.mode` (например, `'charts'`), где значением 
                является словарь с результатами работы каждого успешного обработчика.

        Examples:
            Результат выполнения функции будет иметь следующую структуру:
            {
                "charts": {
                    "line_chart": {"labels": [...], "datasets": [...]},
                    "bar_chart": {"labels": [...], "datasets": [...]}
                }
            }
        """
        init_cls = {}
        
        for name, value in payload.model_dump(exclude_none=True).items():
            handler = self.handlers.get(name)  
            if handler is None:
                logger.warning(f"Обработчик для графика '{name}' не найден в реестре!")
                continue
            init_cls[name] = asyncio.create_task(
                handler.build(user_id, value)
            )
        data = await gather_named(init_cls)
        return {
            self.mode: data
        }

    @staticmethod   
    async def gather_named(tasks: dict):
        """Асинхронно выполняет словарь задач и возвращает их результаты с сохранением имен.

        Функция является безопасной оберткой над `asyncio.gather`. Если одна из задач 
        завершается ошибкой, приложение не падает: исключение перехватывается, 
        логируется, а вместо результата для этой задачи записывается `None`.

        Args:
            tasks: Словарь, где ключ — понятное строковое имя задачи (например, 'get_users'), 
                а значение — объект корутины или запущенной Task.

        Returns:
            dict: Словарь с результатами выполнения, где ключи полностью соответствуют 
                входному словарю `tasks`, а значения — результаты выполнения соответствующих задач.
        """
        result = await asyncio.gather(*tasks.values(), return_exceptions=True)
        data = {}
        for name, res in zip(tasks.keys(), result):
            if isinstance(res, Exception):
                logger.error(f"{name}: {str(res)}")
                data[name] = None
            else:
                data[name] = res
        return data