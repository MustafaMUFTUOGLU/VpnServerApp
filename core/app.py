import os
from fastapi_redis_cache import FastApiRedisCache

redis_cache = FastApiRedisCache()
redis_cache.init(
        host_url=os.environ.get("CACHE_REDIS_URL")
    )
