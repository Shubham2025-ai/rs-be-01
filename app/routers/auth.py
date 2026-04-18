from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse
from app import auth

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

security = HTTPBearer()

# ── Register ──────────────────────────────
@router.post("/register", status_code=201)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(
        username=user.username,
        hashed_password=auth.hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "username": new_user.username, "role": new_user.role}

# ── Login ─────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = auth.create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer", "role": db_user.role}

# ── Get Current User ──────────────────────
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = auth.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

# ── Admin only dependency ─────────────────
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user