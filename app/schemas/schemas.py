from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class StatusEnum(str, Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRY = "RETRY"

# ── Auth Schemas ──────────────────────────
class UserRegister(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.VIEWER

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

# ── Execution Schemas ─────────────────────
class ExecutionCreate(BaseModel):
    job_id: str
    job_name: str
    input_params: Optional[str] = None
    tags: Optional[str] = None

class ExecutionUpdate(BaseModel):
    status: StatusEnum
    output_summary: Optional[str] = None
    error_details: Optional[str] = None
    duration_ms: Optional[int] = None

class ExecutionResponse(BaseModel):
    id: str
    job_id: str
    job_name: str
    triggered_by: str
    status: str
    input_params: Optional[str]
    tags: Optional[str]

    model_config = {"from_attributes": True}