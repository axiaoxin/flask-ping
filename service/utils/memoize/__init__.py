from redis import Redis

import settings
from .core import Memoizer
from .redis import wrap

redis_client = Redis.from_url(settings.REDIS_URL)

redis_memoize = Memoizer(wrap(redis_client))
