from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import AuditEvent, ExecutionRecord
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/executions", tags=["Audit Trail"])

# ── Get Audit Trail for specific execution ─────────────────────
@router.get("/{execution_id}/audit")
def get_audit_trail(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check execution exists
    execution = db.query(ExecutionRecord).filter(
        ExecutionRecord.id == execution_id
    ).first()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    # Get all audit events for this execution
    audit_events = db.query(AuditEvent).filter(
        AuditEvent.execution_id == execution_id
    ).order_by(AuditEvent.timestamp.asc()).all()

    return {
        "execution_id": execution_id,
        "job_name": execution.job_name,
        "total_events": len(audit_events),
        "audit_trail": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "actor": event.actor,
                "event_metadata": event.event_metadata
            }
            for event in audit_events
        ]
    }