FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements if exists
COPY requirements.txt* ./

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
RUN pip install --no-cache-dir \
    celery[redis] \
    sqlalchemy \
    psycopg2-binary \
    redis \
    requests \
    croniter

# Copy application code
COPY . .

# Expose port if needed
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Default command
CMD ["celery", "-A", "scheduler", "beat", "--loglevel=info"]
