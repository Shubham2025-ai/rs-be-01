from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base, SessionLocal
from app.models import models
from app.routers import auth, executions, audit, summary
from app.messaging import start_consumer

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_consumer(SessionLocal)
    print("RabbitMQ consumer started in background!")
    yield
    # Shutdown (nothing needed)

app = FastAPI(
    title="RS-BE-01 Execution Tracking and Audit Service",
    description="Backend service for tracking pipeline executions and audit logs",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(executions.router)
app.include_router(audit.router)
app.include_router(summary.router)

@app.get("/")
def root():
    return {"message": "RS-BE-01 Service is running!"}