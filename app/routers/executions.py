from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.models.models import ExecutionRecord, AuditEvent, StatusEnum
from app.schemas.schemas import ExecutionCreate, ExecutionUpdate, ExecutionResponse
from app.routers.auth import get_current_user
from datetime import datetime
from typing import Optional
import uuid

router = APIRouter(prefix="/api/v1/executions", tags=["Executions"])

# ── Create Execution ──────────────────────────────────────────
@router.post("/", status_code=201)
def create_execution(
    payload: ExecutionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    execution = ExecutionRecord(
        id=str(uuid.uuid4()),
        job_id=payload.job_id,
        job_name=payload.job_name,
        triggered_by=current_user["username"],
        status=StatusEnum.STARTED,
        start_time=datetime.utcnow(),
        input_params=payload.input_params,
        tags=payload.tags
    )
    db.add(execution)

    # Write audit event
    audit = AuditEvent(
        id=str(uuid.uuid4()),
        execution_id=execution.id,
        event_type="EXECUTION_STARTED",
        timestamp=datetime.utcnow(),
        actor=current_user["username"],
        event_metadata=f"Job '{payload.job_name}' started"
    )
    db.add(audit)
    db.commit()
    db.refresh(execution)

    return {
        "message": "Execution created successfully",
        "execution_id": execution.id,
        "job_name": execution.job_name,
        "status": execution.status,
        "triggered_by": execution.triggered_by,
        "start_time": execution.start_time
    }

# ── Update Execution Status ───────────────────────────────────
@router.patch("/{execution_id}")
def update_execution(
    execution_id: str,
    payload: ExecutionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    execution = db.query(ExecutionRecord).filter(
        ExecutionRecord.id == execution_id
    ).first()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    execution.status = payload.status
    execution.output_summary = payload.output_summary
    execution.error_details = payload.error_details
    execution.duration_ms = payload.duration_ms

    if payload.status in [StatusEnum.SUCCESS, StatusEnum.FAILED]:
        execution.end_time = datetime.utcnow()

    # Write audit event
    audit = AuditEvent(
        id=str(uuid.uuid4()),
        execution_id=execution_id,
        event_type=f"STATUS_CHANGED_TO_{payload.status}",
        timestamp=datetime.utcnow(),
        actor=current_user["username"],
        event_metadata=f"Status updated to {payload.status}"
    )
    db.add(audit)
    db.commit()
    db.refresh(execution)

    return {
        "message": "Execution updated successfully",
        "execution_id": execution.id,
        "status": execution.status,
        "end_time": execution.end_time,
        "duration_ms": execution.duration_ms
    }

# ── Get All Executions with Filters ──────────────────────────
@router.get("/")
def get_executions(
    job_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    triggered_by: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(ExecutionRecord)

    # Apply filters
    if job_name:
        query = query.filter(ExecutionRecord.job_name.ilike(f"%{job_name}%"))
    if status:
        query = query.filter(ExecutionRecord.status == status)
    if triggered_by:
        query = query.filter(ExecutionRecord.triggered_by == triggered_by)
    if from_date:
        query = query.filter(ExecutionRecord.start_time >= datetime.fromisoformat(from_date))
    if to_date:
        query = query.filter(ExecutionRecord.start_time <= datetime.fromisoformat(to_date))

    total = query.count()
    executions = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": [
            {
                "id": e.id,
                "job_id": e.job_id,
                "job_name": e.job_name,
                "triggered_by": e.triggered_by,
                "status": e.status,
                "start_time": e.start_time,
                "end_time": e.end_time,
                "duration_ms": e.duration_ms,
                "tags": e.tags
            }
            for e in executions
        ]
    }

# ── Get Single Execution ──────────────────────────────────────
@router.get("/{execution_id}")
def get_execution(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    execution = db.query(ExecutionRecord).filter(
        ExecutionRecord.id == execution_id
    ).first()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return {
        "id": execution.id,
        "job_id": execution.job_id,
        "job_name": execution.job_name,
        "triggered_by": execution.triggered_by,
        "status": execution.status,
        "start_time": execution.start_time,
        "end_time": execution.end_time,
        "duration_ms": execution.duration_ms,
        "input_params": execution.input_params,
        "output_summary": execution.output_summary,
        "error_details": execution.error_details,
        "tags": execution.tags
    }