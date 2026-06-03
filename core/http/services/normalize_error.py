from core.logger.logger import logger

def normalize_error(text: str, status:int) -> str:
    logger.error(text)
    text = (text or '').strip()
    if status == 401:
        return text or '401 Unauthorized'
    if status == 403:
        return text or '403 Forbidden'
    if status == 404:
        return text or '404 Not Found'
    if status == 429:
        return text or '429 Too Many Requests'
    if status == 502:
        return '502 Bad Gateway'
    if status == 504:
        return '504 Gateway Timeout'
    if status >= 500:
        if 'Bad Gateway' in text:
            return '502 Bad Gateway'
        if 'Gateway Timeout' in text:
            return '504 Gateway Timeout'
        return text[:100] if text else f'{status} Server Error'

    return text[:100] if text else f'HTTP {status}'
    
