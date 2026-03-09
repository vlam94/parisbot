# Superset Flask Configuration
# https://superset.apache.org/docs/installation/configuring-superset

import os
from datetime import timedelta

# Flask Configuration
DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'dev-secret-key-change-in-production')
FLASK_ENV = 'production'

# Database Configuration
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SUPERSET_DATABASE_URI',
    'postgresql://superset:superset_pass@superset-database:5433/superset'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Redis Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://superset-cache:6380/0',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 24 hours
}

# Redis Result Backend Configuration
RESULTS_BACKEND = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://superset-cache:6380/1',
    'CACHE_DEFAULT_TIMEOUT': 86400,
}

# Celery Configuration
CELERY_CONFIG = {
    'broker_url': 'redis://superset-cache:6380/2',
    'result_backend': 'redis://superset-cache:6380/3',
    'task_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 30 * 60,  # 30 minutes
    'task_soft_time_limit': 25 * 60,  # 25 minutes
}

# Session Configuration
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

# Security
ENABLE_PROXY_FIX = True
PREVENT_UNSAFE_DB_CONNECTIONS = True
ALLOWED_EXTRA_DATASOURCE_HEADERS = ['Authorization']

# Feature Flags
FEATURE_FLAGS = {
    'ALLOW_ADHOC_SUBQUERY': False,
    'ENABLE_JAVASCRIPT_CONTROLS': False,
    'SQLLAB_BACKEND_PERSISTENCE': True,
    'VERSIONED_EXPORT': True,
    'DASHBOARD_RBAC': True,
    'DASHBOARDS_CACHING': True,
}

# Data Source Configuration
DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://superset-cache:6380/4',
    'CACHE_DEFAULT_TIMEOUT': 3600,  # 1 hour
}

# Email Configuration
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', False)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@superset.local')

# Logging Configuration
LOG_FORMAT = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
LOG_LEVEL = 'INFO'

# API Configuration
API_PAGE_SIZE_LIMIT = 100

# Map Configuration
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY', '')

# Limit Configurations
ROW_LIMIT = 50000
DISPLAY_MAX_ROW = 10000
SQL_CELERY_DB_RESULTS_BACKEND = {
    'type': 'cache',
    'location': 'redis://superset-cache:6380/5'
}

# Default Roles/Permissions
DEFAULT_ROLE = 'Public'

# Allow public access (set to False in production)
PUBLIC_ROLE_LIKE_GAMMA = False

# Session Timeout (in minutes)
SESSION_TIMEOUT_MINUTES = 1440  # 24 hours
