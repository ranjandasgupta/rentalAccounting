from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..crud import CRUD

router = APIRouter(prefix="/api", tags=["accounts"])

crud_type = CRUD(models.AccountType)
crud_subtype = CRUD(models.AccountSubType)
crud_account = CRUD(models.Account)

@router.get("/account-types", response_model=List[schemas.AccountTypeRead])
def list_account_types(db: Session = Depends(get_db)):
    return crud_type.list(db)

@router.post("/account-types", response_model=schemas.AccountTypeRead)
def create_account_type(body: schemas.AccountTypeCreate, db: Session = Depends(get_db)):
    return crud_type.create(db, body.model_dump())

@router.get("/account-subtypes", response_model=List[schemas.AccountSubTypeRead])
def list_account_subtypes(db: Session = Depends(get_db)):
    return crud_subtype.list(db)

@router.post("/account-subtypes", response_model=schemas.AccountSubTypeRead)
def create_account_subtype(body: schemas.AccountSubTypeCreate, db: Session = Depends(get_db)):
    return crud_subtype.create(db, body.model_dump())

@router.get("/accounts", response_model=List[schemas.AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return crud_account.list(db)

@router.post("/accounts", response_model=schemas.AccountRead)
def create_account(body: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud_account.create(db, body.model_dump())
