# RS-BE-01 — Execution Tracking and Audit Service

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7.4-red?style=for-the-badge&logo=redis)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.13-orange?style=for-the-badge&logo=rabbitmq)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)

---

## 🌐 Live Deployment

| Resource | Link |
|---|---|
| 🚀 Live API | https://rs-be-01.onrender.com |
| 📖 Swagger Docs | https://rs-be-01.onrender.com/docs |
| 🔗 GitHub | https://github.com/Shubham2025-ai/rs-be-01 |

---

## 📌 Project Overview

**RS-BE-01** is a production-grade backend microservice developed for **Rubiscape** as part of an industry-collaborative project. It provides a centralized, scalable, and secure platform for tracking pipeline execution events, generating immutable audit logs, and delivering real-time analytics — all exposed through a clean RESTful API with auto-generated Swagger documentation.

> Built entirely in Python using FastAPI, this service demonstrates enterprise-grade backend engineering including message queue integration, distributed caching, role-based security, and containerized deployment.

---

## 📋 Project Info

| Field | Details |
|---|---|
| Project ID | RS-BE-01 |
| Company | Rubiscape |
| College | Vishwakarma Institute of Technology, Pune |
| Team Size | 3 Students |
| Tech Stack | Python, FastAPI, PostgreSQL, Redis, RabbitMQ, Docker |
| Deployment | Render (Cloud) |
| Status | ✅ Live & Active |
| Academic Year | 2025–2026 |

---

## ✅ Features Delivered

| Feature | Status | Details |
|---|---|---|
| RESTful API | ✅ Complete | Full CRUD for execution records |
| Real-time Event Ingestion | ✅ Complete | REST + RabbitMQ message queue |
| Immutable Audit Trail | ✅ Complete | Append-only audit log per execution |
| Query Engine | ✅ Complete | Filter by job, status, date, user, tags |
| Pagination | ✅ Complete | Page + limit with total pages |
| Summary Analytics | ✅ Complete | Success rate, avg duration, top failed jobs |
| JWT Authentication | ✅ Complete | Secure token-based login |
| Role Based Access Control | ✅ Complete | Admin / Analyst / Viewer roles |
| Redis Caching | ✅ Complete | Summary stats cached for 60 seconds |
| RabbitMQ Integration | ✅ Complete | Async event queue with background consumer |
| Swagger / OpenAPI Docs | ✅ Complete | Auto-generated, interactive |
| Unit & Integration Tests | ✅ Complete | 15/15 passing with Pytest |
| Docker Containerization | ✅ Complete | 4-container setup with docker-compose |
| Cloud Deployment | ✅ Complete | Live on Render with cloud DB, Redis, RabbitMQ |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT / SWAGGER UI                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Requests
┌─────────────────────────▼───────────────────────────────────┐
│                    API LAYER (FastAPI)                        │
│  ┌──────────┐  ┌────────────┐  ┌───────────┐  ┌──────────┐ │
│  │   Auth   │  │ Executions │  │   Audit   │  │ Summary  │ │
│  │ Register │  │   CRUD +   │  │   Trail   │  │Analytics │ │
│  │  Login   │  │  Filters   │  │ Immutable │  │  Cache   │ │
│  └──────────┘  └────────────┘  └───────────┘  └──────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  SERVICE LAYER (Business Logic)               │
│     JWT Auth │ RBAC │ Event Processing │ Aggregation          │
└──────┬────────────────────────────┬────────────────┬─────────┘
       │                            │                │
┌──────▼──────┐           ┌────────▼──────┐  ┌─────▼────────┐
│  PostgreSQL │           │   RabbitMQ    │  │    Redis     │
│  Primary DB │           │  Message Queue│  │    Cache     │
│             │           │               │  │              │
│ Executions  │           │ Async Event   │  │ Summary      │
│ Audit Logs  │           │ Ingestion     │  │ Stats 60s    │
│ Users       │           │ Background    │  │ TTL          │
└─────────────┘           └───────────────┘  └──────────────┘
```

---

## 🗄️ Database Schema

### ExecutionRecord
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| job_id | String | Pipeline job identifier |
| job_name | String | Human readable job name |
| triggered_by | String | User who triggered |
| status | Enum | STARTED / RUNNING / SUCCESS / FAILED / RETRY |
| start_time | DateTime | Execution start timestamp |
| end_time | DateTime | Execution end timestamp |
| duration_ms | Integer | Total duration in milliseconds |
| input_params | Text | Input parameters |
| output_summary | Text | Output summary |
| error_details | Text | Error info if failed |
| tags | String | Tags for filtering |

### AuditEvent — Append Only, Never Deleted
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| execution_id | String | Reference to execution |
| event_type | String | EXECUTION_STARTED, STATUS_CHANGED, etc. |
| timestamp | DateTime | Exact event timestamp |
| actor | String | User or system that triggered |
| event_metadata | Text | Additional context |

### User
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| username | String | Unique username |
| hashed_password | String | Bcrypt hashed |
| role | Enum | ADMIN / ANALYST / VIEWER |
| created_at | DateTime | Creation timestamp |

---

## 🔐 Role Based Access Control

| Endpoint | ADMIN | ANALYST | VIEWER |
|---|:---:|:---:|:---:|
| POST /executions | ✅ | ❌ | ❌ |
| PATCH /executions/:id | ✅ | ❌ | ❌ |
| GET /executions | ✅ | ✅ | ✅ |
| GET /executions/:id | ✅ | ✅ | ✅ |
| GET /executions/:id/audit | ✅ | ✅ | ❌ |
| GET /executions/summary/stats | ✅ | ✅ | ❌ |

---

## 📡 API Reference

### Authentication
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /api/v1/auth/register | Register new user | None |
| POST | /api/v1/auth/login | Login + get JWT | None |

### Executions
| Method | Endpoint | Description | Min Role |
|---|---|---|---|
| POST | /api/v1/executions/ | Create execution | ADMIN |
| PATCH | /api/v1/executions/{id} | Update status | ADMIN |
| GET | /api/v1/executions/ | List + filter | VIEWER |
| GET | /api/v1/executions/{id} | Get single | VIEWER |

### Audit & Analytics
| Method | Endpoint | Description | Min Role |
|---|---|---|---|
| GET | /api/v1/executions/{id}/audit | Audit trail | ANALYST |
| GET | /api/v1/executions/summary/stats | Analytics | ANALYST |

### Query Filters
| Filter | Example |
|---|---|
| job_name | ?job_name=Pipeline |
| status | ?status=SUCCESS |
| triggered_by | ?triggered_by=admin |
| tags | ?tags=production |
| from_date | ?from_date=2026-01-01 |
| to_date | ?to_date=2026-12-31 |
| page | ?page=1 |
| limit | ?limit=10 |

---

## 🐇 RabbitMQ Event Flow

```
POST /api/v1/executions
        ↓
FastAPI saves to PostgreSQL
        ↓
Publishes event → RabbitMQ Queue
        ↓
Background Consumer reads event
        ↓
Saves AuditEvent to PostgreSQL
        ↓
Acknowledges message
```

**Events:** `EXECUTION_CREATED` | `EXECUTION_UPDATED_{STATUS}`

---

## ⚡ Redis Cache Flow

```
GET /api/v1/executions/summary/stats
        ↓
   [Cache HIT]          [Cache MISS]
source: "cache" ⚡    Query PostgreSQL
                      Store in Redis (60s TTL)
                      source: "database"

Cache cleared on: new execution or status update
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python + FastAPI | High-performance async REST API |
| Database | PostgreSQL 15 | ACID-compliant primary store |
| ORM | SQLAlchemy 2.0 | Database interactions |
| Cache | Redis 7.4 | In-memory caching layer |
| Message Queue | RabbitMQ 3.13 | Async event ingestion |
| Auth | JWT + bcrypt | Secure stateless authentication |
| Container | Docker + Compose | Multi-service orchestration |
| Testing | Pytest + HTTPX | Automated test suite |
| Docs | Swagger UI | Auto-generated API docs |
| Deployment | Render | Cloud production hosting |

---

## 🏗️ Project Structure

```
rs-be-01/
├── app/
│   ├── routers/
│   │   ├── auth.py          → Auth endpoints + RBAC deps
│   │   ├── executions.py    → Execution CRUD + filters
│   │   ├── audit.py         → Audit trail endpoints
│   │   └── summary.py       → Analytics + Redis cache
│   ├── models/
│   │   └── models.py        → Database models
│   ├── schemas/
│   │   └── schemas.py       → Pydantic schemas
│   ├── database.py          → PostgreSQL connection
│   ├── auth.py              → JWT + bcrypt
│   ├── cache.py             → Redis cache logic
│   ├── messaging.py         → RabbitMQ publisher + consumer
│   └── main.py              → App entry point
├── tests/
│   ├── conftest.py          → Test fixtures
│   ├── test_auth.py         → Auth tests (5)
│   ├── test_executions.py   → Execution tests (7)
│   └── test_audit.py        → Audit + summary tests (3)
├── Dockerfile               → Python 3.12 container
├── docker-compose.yml       → 4-service orchestration
├── runtime.txt              → Python version for Render
├── render.yaml              → Render config
├── requirements.txt         → Dependencies
└── README.md
```

---

## 🧪 Test Results

```
pytest tests/ -v

tests/test_audit.py::test_get_audit_trail               PASSED
tests/test_audit.py::test_audit_trail_not_found         PASSED
tests/test_audit.py::test_summary_stats                 PASSED
tests/test_auth.py::test_register_success               PASSED
tests/test_auth.py::test_register_duplicate             PASSED
tests/test_auth.py::test_login_success                  PASSED
tests/test_auth.py::test_login_wrong_password           PASSED
tests/test_auth.py::test_login_wrong_username           PASSED
tests/test_executions.py::test_create_execution         PASSED
tests/test_executions.py::test_create_execution_no_auth PASSED
tests/test_executions.py::test_get_executions           PASSED
tests/test_executions.py::test_get_executions_filter    PASSED
tests/test_executions.py::test_update_execution         PASSED
tests/test_executions.py::test_update_not_found         PASSED
tests/test_executions.py::test_get_single_execution     PASSED

================== 15 passed in 3.26s ==================
```

---

## 🐳 Docker Setup

```bash
# Clone and run with Docker
git clone https://github.com/Shubham2025-ai/rs-be-01.git
cd rs-be-01
docker-compose up --build
```

**4 containers start automatically:**
- `rs_be_01_app` → FastAPI on port 8000
- `rs_be_01_db` → PostgreSQL on port 5432
- `rs_be_01_redis` → Redis on port 6379
- `rs_be_01_rabbitmq` → RabbitMQ on port 5672

Open: **http://localhost:8000/docs**

---

## 🛠️ Local Setup

```bash
# 1. Clone
git clone https://github.com/Shubham2025-ai/rs-be-01.git
cd rs-be-01

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Create .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/rs_be_01
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=localhost
REDIS_PORT=6379
RABBITMQ_URL=amqp://guest:guest@localhost/

# 5. Run
uvicorn app.main:app

# 6. Test
pytest tests/ -v
```

---

## 📊 Objectives — Delivery Status

| # | Objective | Metric | Status |
|---|---|---|---|
| O1 | Centralized Execution Tracking | Real-time ingestion via REST + RabbitMQ | ✅ |
| O2 | Immutable Audit Trail | Append-only — zero data loss | ✅ |
| O3 | Queryable Execution History | 6 filters + pagination | ✅ |
| O4 | Failure Analytics | Success rate, avg duration, top failures | ✅ |
| O5 | Secure Access Control | JWT + 3-tier RBAC — all endpoints protected | ✅ |

---

## 👥 Team

| Name | Role | Contribution |
|---|---|---|
| Shubham | Team Lead / Backend Developer | Full architecture, all APIs, database, auth, RBAC, Redis, RabbitMQ, Docker, deployment, testing, documentation |
| Pranav Bhoyate | Backend Developer | Code review, testing support |
| Ansh Bhujbal | Backend Developer | Documentation support |

---

## 🏢 Project Details

- **College:** Vishwakarma Institute of Technology, Pune
- **Industry Partner:** Rubiscape
- **Project ID:** RS-BE-01
- **Academic Year:** 2025–2026