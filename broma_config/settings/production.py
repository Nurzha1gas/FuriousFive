import environ

# Assuming .local contains base settings and imports, like base.py in many projects
from .local import *

"""
Configures Django settings using environment variables.

- SECRET_KEY, DEBUG, DATABASES, and ALLOWED_HOSTS are set via environment variables.
- CHANNEL_LAYERS configures Django Channels with Redis for real-time functionality.
"""

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),  # Cast and default value
)

# Secret Key: ensure this is set in Heroku's config vars
SECRET_KEY = env('SECRET_KEY')

# Debug: should be set to False in production
DEBUG = env.bool('DEBUG', default=False)

# Databases: the DATABASE_URL environment variable is provided by Heroku if you add a database addon
DATABASES = {
    'default': env.db(),
}

# Allowed Hosts: set this to your Heroku domain and any custom domains
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['qossyl-diploma-4aeb1fe4a29b.herokuapp.com'])

# Redis URL: provided by Heroku if you add a Redis addon
REDIS_URL = env('REDIS_URL')

# Channel Layers: configured to use Redis as the backing store
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    }
}
