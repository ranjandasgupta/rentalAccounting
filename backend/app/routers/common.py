from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok"}
