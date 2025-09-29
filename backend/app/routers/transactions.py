from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..crud import CRUD

router = APIRouter(prefix="/api", tags=["transactions"])

crud_trans = CRUD(models.Transaction)

@router.get("/transactions", response_model=List[schemas.TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    return crud_trans.list(db)

@router.post("/transactions", response_model=schemas.TransactionRead)
def create_transaction(body: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Basic validation
    if body.debit_account_id == body.credit_account_id:
        raise HTTPException(status_code=400, detail="Debit and Credit accounts must differ.")
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive.")
    return crud_trans.create(db, body.model_dump())
