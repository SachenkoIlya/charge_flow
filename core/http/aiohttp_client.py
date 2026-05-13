import aiohttp


def get_client() -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(limit=50, limit_per_host=4, ttl_dns_cache=120)
    timeout = aiohttp.ClientTimeout(total=None, connect=40, sock_connect=30, sock_read=120)
    return aiohttp.ClientSession(connector=connector, timeout=timeout) 
