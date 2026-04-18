from sqlalchemy import Column, String, Integer, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import uuid
import enum

class StatusEnum(str, enum.Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRY = "RETRY"

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

# Main execution record table
class ExecutionRecord(Base):
    __tablename__ = "execution_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, nullable=False)
    job_name = Column(String, nullable=False)
    triggered_by = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.STARTED)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    input_params = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=True)
    error_details = Column(Text, nullable=True)
    tags = Column(String, nullable=True)

# Audit log table — append only, never delete
class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    actor = Column(String, nullable=False)
    event_metadata = Column(Text, nullable=True)  # ← renamed from metadata

# User table for auth
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.VIEWER)
    created_at = Column(DateTime, default=func.now())