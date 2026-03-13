# 🌦 Weather DataOps Project

## 🎯 Goal
This project applies **DataOps and infrastructure knowledge** to build a simple **weather data retrieval application** using **Airflow, Postgres, and Superset**. The idea is to start locally with **Docker Compose** and then deploy to a **free-tier cloud infrastructure** to test scalability, maintainability, and integration skills.

The project demonstrates:
- Modular architecture with Docker Compose
- Data pipeline orchestration using Airflow
- Persistent storage with Postgres
- Interactive dashboards with Superset
- Cloud deployment for real-world testing

---

## 🗂 Project Structure

### 1. Database (Postgres 18)
- Persistent volumes for weather data
- Configurable access via `pg_hba.conf`

### 2. Data Pipeline (Airflow 3.1)
- DAGs for weather data retrieval and transformation
- Modular operators and utilities
- Separate Postgres instance for Airflow metadata

### 3. Data Visualiser (Superset 6)
- Dashboards for weather insights
- Redis cache for performance
- Separate Postgres instance for Superset metadata

---

## 🐳 Docker Compose Guidelines
- Shared network: `parisbot-net`
- Resource limits: **3 CPU cores** and **6 GB RAM**
- Persistent volumes for Postgres and Redis
- `.env` file for secrets and environment variables
- Modular `Dockerfile` and `service.json` per service
- Startup order defined with `depends_on`

---

## ✅ Best Practices
- **Security**: credentials in `.env`, restricted Postgres access, non-root users
- **Modularity**: each module isolated with its own config
- **Maintainability**: documented services, structured directories for future code

---

## 📅 Quick Implementation Plan

1. **Create and Test Airflow**
   - Scaffold DAGs for weather API retrieval
   - Validate scheduling and task execution
   - Connect to Airflow’s Postgres instance

2. **Create and Test Database**
   - Set up Postgres schema for weather data
   - Ensure persistence with volumes
   - Test ingestion from Airflow DAGs

3. **Create and Test Superset**
   - Configure Superset with its own Postgres
   - Build initial dashboards for weather trends
   - Validate Redis caching

4. **Implement Project Tools**
   - precommit
   - poetry

5. **Deploy in Free-Tier Cloud**
   - Choose a free-tier cloud 
   - Deploy Docker Compose stack
   - Test networking, scaling, and persistence

6. **Implement Integrations**
   - Add reporting via chat (Slack/Teams webhook)
   - Integrate simple ML analisys
   - Automate daily reports from Airflow

---

## 🚀 Next Steps
- Start locally with Docker Compose
- Validate each module independently
- Deploy to cloud and test integrations
- Iterate with improvements in security, scalability, and 