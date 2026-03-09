# Superset configuration file

import os
from datetime import timedelta

# Flask app config
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'change-me-in-production')
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SUPERSET_DATABASE_URI',
    'postgresql://superset:superset_pass@superset-db:5432/superset'
)

# Redis cache config
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
}

# Celery config
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CELERY_BEAT_SCHEDULE = {
    'cache-warmup': {
        'task': 'superset.tasks.cache.warm_up_cache',
        'schedule': timedelta(minutes=30),
    },
}

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_JAVASCRIPT_CONTROLS': True,
    'PRESTO_EXPAND_DATA': True,
}

# Superset config
ROW_LIMIT = 50000
SUPERSET_WEBSERVER_PORT = 8088
