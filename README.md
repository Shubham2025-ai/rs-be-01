Here's the complete README — just copy and paste everything:

```markdown
# RS-BE-01 — Execution Tracking and Audit Service

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Redis](https://img.shields.io/badge/Redis-7.4-red)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-4.2-orange)
![Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

A production-grade backend microservice built for **Rubiscape** as part of the industry collaboration project **RS-BE-01**. This service provides centralized execution tracking, immutable audit logging, Redis caching, RabbitMQ message queue integration, and role-based access control for pipeline orchestration systems.

---

## 📌 Project Info

| Field | Details |
|---|---|
| Project ID | RS-BE-01 |
| Company | Rubiscape |
| Team Size | 3 Students |
| Stack | Python, FastAPI, PostgreSQL, Redis, RabbitMQ |
| Status | Active Development |
| Academic Year | 2025–2026 |

---

## 🚀 Features

- ✅ **Execution Tracking** — Real-time ingestion of pipeline execution events
- ✅ **Immutable Audit Trail** — Append-only audit logs for every execution
- ✅ **Query Engine** — Filter executions by job name, status, date, user
- ✅ **Summary Analytics** — Success rate, average duration, top failed jobs
- ✅ **JWT Authentication** — Secure token-based login system
- ✅ **Role Based Access Control** — Admin, Analyst, Viewer roles
- ✅ **Redis Caching** — Summary stats cached for 60 seconds
- ✅ **RabbitMQ Integration** — Async event queue for execution events
- ✅ **Auto Swagger Docs** — Interactive API documentation built-in
- ✅ **15/15 Tests Passing** — Full unit and integration test coverage

---

## 🏗️ Project Structure

```
rs-be-01/
├── app/
│   ├── routers/
│   │   ├── auth.py            → Authentication endpoints
│   │   ├── executions.py      → Execution CRUD endpoints
│   │   ├── audit.py           → Audit trail endpoints
│   │   └── summary.py         → Analytics endpoints
│   ├── models/
│   │   └── models.py          → Database table definitions
│   ├── schemas/
│   │   └── schemas.py         → Request/Response validation
│   ├── database.py            → PostgreSQL connection
│   ├── auth.py                → JWT + bcrypt logic
│   ├── cache.py               → Redis caching logic
│   ├── messaging.py           → RabbitMQ publisher + consumer
│   └── main.py                → App entry point
├── tests/
│   ├── conftest.py            → Test configuration
│   ├── test_auth.py           → Auth tests
│   ├── test_executions.py     → Execution API tests
│   └── test_audit.py          → Audit + Summary tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python + FastAPI | REST API framework |
| Database | PostgreSQL | Primary data store |
| ORM | SQLAlchemy + Alembic | Database interactions |
| Cache | Redis | Summary stats caching |
| Message Queue | RabbitMQ | Async event ingestion |
| Auth | JWT + bcrypt | Authentication & hashing |
| Testing | Pytest + HTTPX | Unit & integration tests |
| Docs | Swagger UI | Auto API documentation |
| Container | Docker + Compose | Deployment |

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
| start_time | DateTime | Execution start time |
| end_time | DateTime | Execution end time |
| duration_ms | Integer | Duration in milliseconds |
| input_params | Text | Input parameters |
| output_summary | Text | Output summary |
| error_details | Text | Error info if failed |
| tags | String | Execution tags |

### AuditEvent
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| execution_id | String | Reference to execution |
| event_type | String | Type of event |
| timestamp | DateTime | When event occurred |
| actor | String | Who performed action |
| event_metadata | Text | Additional info |

### User
| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| username | String | Unique username |
| hashed_password | String | Bcrypt hashed password |
| role | Enum | ADMIN / ANALYST / VIEWER |
| created_at | DateTime | Account creation time |

---

## 🔐 Role Based Access Control

| Endpoint | ADMIN | ANALYST | VIEWER |
|---|---|---|---|
| POST /executions | ✅ | ❌ | ❌ |
| PATCH /executions/:id | ✅ | ❌ | ❌ |
| GET /executions | ✅ | ✅ | ✅ |
| GET /executions/:id | ✅ | ✅ | ✅ |
| GET /executions/:id/audit | ✅ | ✅ | ❌ |
| GET /executions/summary/stats | ✅ | ✅ | ❌ |

---

## 🐇 RabbitMQ Message Flow

```
Pipeline Job
     ↓
POST /api/v1/executions  (REST API)
     ↓
FastAPI publishes event → RabbitMQ Queue
     ↓
Background Consumer reads event
     ↓
Saves AuditEvent to PostgreSQL
```

---

## ⚡ Redis Cache Flow

```
GET /api/v1/executions/summary/stats
     ↓
Check Redis cache
     ↓ (miss)              ↓ (hit)
Query PostgreSQL      Return cached data
     ↓                (source: cache ⚡)
Store in Redis
(expires: 60s)
     ↓
Return data
(source: database)
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /api/v1/auth/register | Register new user | None |
| POST | /api/v1/auth/login | Login + get JWT token | None |

### Executions
| Method | Endpoint | Description | Role |
|---|---|---|---|
| POST | /api/v1/executions/ | Create execution record | ADMIN |
| PATCH | /api/v1/executions/:id | Update execution status | ADMIN |
| GET | /api/v1/executions/ | Get all with filters | VIEWER+ |
| GET | /api/v1/executions/:id | Get single execution | VIEWER+ |

### Audit & Analytics
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | /api/v1/executions/:id/audit | Full audit trail | ANALYST+ |
| GET | /api/v1/executions/summary/stats | Analytics summary | ANALYST+ |

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- Redis
- RabbitMQ + Erlang
- Git

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Shubham2025-ai/rs-be-01.git
cd rs-be-01
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file:**
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/rs_be_01
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=localhost
REDIS_PORT=6379
```

**5. Create database in pgAdmin:**
```
Database name: rs_be_01
```

**6. Start Redis:**
```bash
redis-server
```

**7. Start RabbitMQ:**
```bash
rabbitmq-service start
```

**8. Run the server:**
```bash
uvicorn app.main:app
```

**9. Open Swagger docs:**
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Expected output:
```
15 passed, 0 failed
```

---

## 👥 Team

| Name | Role | Contribution |
|---|---|---|
| Shubham | Team Lead / Backend Developer | Architecture, all API development, database design, JWT auth, RBAC, Redis caching, RabbitMQ integration, testing, documentation |
| Pranav Bhoyate | Backend Developer | Code review, testing support |
| Ansh Bhujbal | Backend Developer | Documentation support |

---

## 🏢 Project Details

- **College:** Vishwakarma Institute of Technology, Pune
- **Company:** Rubiscape
- **Project ID:** RS-BE-01
- **Academic Year:** 2025–2026