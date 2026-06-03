import aiohttp


def get_client() -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(
        limit=20, 
        limit_per_host=2, 
        ttl_dns_cache=120
    )
    timeout = aiohttp.ClientTimeout(
        total=12, 
        connect=5, 
        sock_connect=5, 
        sock_read=7
    )
    return aiohttp.ClientSession(
        connector=connector, 
        timeout=timeout
    ) 
