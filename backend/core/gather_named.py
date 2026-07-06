from core.logger.logger import logger
import asyncio



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