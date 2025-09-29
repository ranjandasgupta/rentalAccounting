from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..audits import run_all_audits

router = APIRouter(prefix="/api/audits", tags=["audits"])

@router.get("")
def run_audits(db: Session = Depends(get_db)):
    return run_all_audits(db)
