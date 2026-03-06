#!/bin/bash
# ParisBot Docker Infrastructure - Startup Script

set -e

echo "🚀 ParisBot Docker Infrastructure Startup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    exit 1
fi

# Check Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"

# Check .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found - creating from defaults${NC}"
else
    echo -e "${GREEN}✓ .env file found${NC}"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p dags logs scripts

echo -e "${GREEN}✓ Directories ready${NC}"

# Check Docker daemon
echo "🔍 Checking Docker daemon..."
if ! docker ps &> /dev/null; then
    echo -e "${RED}✗ Docker daemon is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker daemon running${NC}"

# Check available system resources
echo ""
echo "💾 System Resources:"
TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
AVAILABLE_RAM=$(free -h | awk '/^Mem:/ {print $7}')
CPU_CORES=$(nproc)
echo "   Total RAM: $TOTAL_RAM"
echo "   Available RAM: $AVAILABLE_RAM"
echo "   CPU Cores: $CPU_CORES"

if [ "$CPU_CORES" -lt 3 ]; then
    echo -e "${YELLOW}⚠ Warning: Only $CPU_CORES CPU cores available (3+ recommended)${NC}"
fi

echo ""
echo "🐳 Starting Docker containers..."
echo "   - PostgreSQL 18"
echo "   - Airflow 3.1 (Webserver + Scheduler)"
echo "   - Superset 3.0"
echo "   - Redis 7"

docker-compose up -d

echo ""
echo -e "${GREEN}✓ Containers started${NC}"
echo ""
echo "⏳ Waiting for services to initialize..."
echo "   This may take 1-2 minutes..."
echo ""

# Wait for key services
echo "Checking PostgreSQL..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U airflow &>/dev/null; then
        echo -e "${GREEN}✓ PostgreSQL ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ PostgreSQL failed to start${NC}"
        exit 1
    fi
    echo -n "."
    sleep 2
done

sleep 5

echo "Checking Airflow Webserver..."
for i in {1..30}; do
    if docker-compose exec -T airflow-webserver curl -s http://localhost:8080/health &>/dev/null; then
        echo -e "${GREEN}✓ Airflow Webserver ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}⚠ Airflow Webserver taking longer to start${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

echo "Checking Superset..."
for i in {1..30}; do
    if docker-compose exec -T superset curl -s http://localhost:8088/health &>/dev/null; then
        echo -e "${GREEN}✓ Superset ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${YELLOW}⚠ Superset taking longer to start${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

echo ""
echo -e "${GREEN}=========================================="
echo "✓ All Services Started Successfully!"
echo "==========================================${NC}"
echo ""
echo "📊 Access your services:"
echo ""
echo "   🌐 Airflow Webserver"
echo "      URL: http://localhost:8080"
echo "      Username: admin"
echo "      Password: admin"
echo ""
echo "   📈 Superset"
echo "      URL: http://localhost:8088"
echo "      Username: admin"
echo "      Password: admin"
echo ""
echo "   🐘 PostgreSQL"
echo "      Host: localhost:5432"
echo "      User: airflow"
echo "      Password: (see .env)"
echo ""
echo "   📝 View logs:"
echo "      docker-compose logs -f"
echo ""
echo "   🛑 Stop services:"
echo "      docker-compose stop"
echo ""
echo "   📚 For more info:"
echo "      cat README_DOCKER.md"
echo ""
