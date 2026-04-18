from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import ExecutionRecord, StatusEnum
from app.routers.auth import get_current_user
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v1/executions", tags=["Summary Analytics"])

# ── Execution Summary ──────────────────────────────────────────
@router.get("/summary/stats")
def get_summary(
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(ExecutionRecord)

    # Apply date filters if provided
    if from_date:
        query = query.filter(
            ExecutionRecord.start_time >= datetime.fromisoformat(from_date)
        )
    if to_date:
        query = query.filter(
            ExecutionRecord.start_time <= datetime.fromisoformat(to_date)
        )

    total = query.count()
    success = query.filter(ExecutionRecord.status == StatusEnum.SUCCESS).count()
    failed = query.filter(ExecutionRecord.status == StatusEnum.FAILED).count()
    running = query.filter(ExecutionRecord.status == StatusEnum.RUNNING).count()
    started = query.filter(ExecutionRecord.status == StatusEnum.STARTED).count()
    retry = query.filter(ExecutionRecord.status == StatusEnum.RETRY).count()

    # Average duration (only completed executions)
    avg_duration = db.query(
        func.avg(ExecutionRecord.duration_ms)
    ).filter(
        ExecutionRecord.duration_ms.isnot(None)
    ).scalar()

    # Success rate
    success_rate = round((success / total * 100), 2) if total > 0 else 0

    # Most failed jobs
    failed_jobs = db.query(
        ExecutionRecord.job_name,
        func.count(ExecutionRecord.id).label("fail_count")
    ).filter(
        ExecutionRecord.status == StatusEnum.FAILED
    ).group_by(
        ExecutionRecord.job_name
    ).order_by(
        func.count(ExecutionRecord.id).desc()
    ).limit(5).all()

    return {
        "total_executions": total,
        "success_count": success,
        "failed_count": failed,
        "running_count": running,
        "started_count": started,
        "retry_count": retry,
        "success_rate_percent": success_rate,
        "average_duration_ms": round(avg_duration, 2) if avg_duration else 0,
        "top_failed_jobs": [
            {"job_name": job.job_name, "fail_count": job.fail_count}
            for job in failed_jobs
        ]
    }