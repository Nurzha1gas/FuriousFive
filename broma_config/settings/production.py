import environ

from .local import *
"""
Configures Django settings using environment variables. 

- SECRET_KEY, DEBUG, DATABASES, and ALLOWED_HOSTS are set via environment variables.
- CHANNEL_LAYERS configures Django Channels with Redis for real-time functionality.
"""

env = environ.Env(
    DEBUG=(bool, False),
)

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")

DATABASES = {
    "default": env.db(),
}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

REDIS_URL = env("REDIS_URL")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    }
}
