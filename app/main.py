from fastapi import FastAPI
from app.database import engine, Base
from app.models import models
from app.routers import auth, executions, audit, summary

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RS-BE-01 Execution Tracking and Audit Service",
    description="Backend service for tracking pipeline executions and audit logs",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(executions.router)
app.include_router(audit.router)
app.include_router(summary.router)

@app.get("/")
def root():
    return {"message": "RS-BE-01 Service is running!"}