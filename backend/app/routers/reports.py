from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from ..reports import income_statement, balance_sheet, expense_report

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/income-statement")
def get_income_statement(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date must be >= start_date")
    return income_statement(db, start_date, end_date)

@router.get("/balance-sheet")
def get_balance_sheet(as_of: date = Query(...), db: Session = Depends(get_db)):
    return balance_sheet(db, as_of)

@router.get("/expense-report")
def get_expense_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date must be >= start_date")
    return expense_report(db, start_date, end_date)
