from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from .models import Transaction, Account, AccountType, Lease

def trial_balance(db: Session, start_date: date | None = None, end_date: date | None = None):
    t = Transaction.__table__
    conds = []
    if start_date: conds.append(t.c.date >= start_date)
    if end_date: conds.append(t.c.date <= end_date)
    rows = db.execute(
        select(
            func.sum(t.c.amount).label("total_debits"),
            func.sum(t.c.amount).label("total_credits")
        ).where(and_(*conds)) if conds else select(
            func.sum(t.c.amount).label("total_debits"),
            func.sum(t.c.amount).label("total_credits")
        )
    ).one()
    # Because each transaction has equal debit and credit, comparing sums separately requires splitting.
    # Compute separate sums:
    debits = db.execute(select(func.sum(t.c.amount)).where(and_(*(conds + [t.c.debit_account_id.is_not(None)])) if conds else t.c.debit_account_id.is_not(None))).scalar() or 0
    credits = db.execute(select(func.sum(t.c.amount)).where(and_(*(conds + [t.c.credit_account_id.is_not(None)])) if conds else t.c.credit_account_id.is_not(None))).scalar() or 0
    passed = abs(float(debits) - float(credits)) < 0.0001
    return {
        "check": "Trial balance (sum debits == sum credits)",
        "passed": passed,
        "details": f"Debits={float(debits):.2f}, Credits={float(credits):.2f}"
    }

def orphan_references(db: Session):
    # Check for transactions referencing non-existent accounts
    t = Transaction.__table__
    a = Account.__table__
    bad_debits = db.execute(
        select(func.count()).select_from(t.outerjoin(a, t.c.debit_account_id == a.c.id)).where(a.c.id.is_(None))
    ).scalar() or 0
    bad_credits = db.execute(
        select(func.count()).select_from(t.outerjoin(a, t.c.credit_account_id == a.c.id)).where(a.c.id.is_(None))
    ).scalar() or 0
    passed = (bad_debits == 0 and bad_credits == 0)
    return {
        "check": "Transactions reference existing accounts",
        "passed": passed,
        "details": f"Missing debit refs={bad_debits}, Missing credit refs={bad_credits}"
    }

def non_positive_amounts(db: Session):
    t = Transaction.__table__
    cnt = db.execute(select(func.count()).where(t.c.amount <= 0)).scalar() or 0
    return {
        "check": "All transaction amounts are positive",
        "passed": cnt == 0,
        "details": f"Non-positive count={cnt}"
    }

def lease_date_consistency(db: Session):
    # If transaction references tenant & property, ensure date within some active lease window if any
    t = Transaction.__table__
    l = Lease.__table__
    # Count transactions that reference tenant & property but have no matching lease period
    cnt = db.execute(
        select(func.count()).select_from(
            t.outerjoin(l, (t.c.tenant_id == l.c.tenant_id) & (t.c.property_id == l.c.property_id) &
                           ( (l.c.to_date.is_(None) & (t.c.date >= l.c.from_date)) |
                             ((t.c.date >= l.c.from_date) & (t.c.date <= l.c.to_date)) ))
        ).where((t.c.tenant_id.is_not(None)) & (t.c.property_id.is_not(None)) & (l.c.id.is_(None)))
    ).scalar() or 0
    return {
        "check": "Transactions tied to tenant & property fall within an active lease (if any lease exists)",
        "passed": cnt == 0,
        "details": f"Out-of-lease transactions={cnt}"
    }

def run_all_audits(db: Session):
    results = [
        trial_balance(db),
        orphan_references(db),
        non_positive_amounts(db),
        lease_date_consistency(db),
    ]
    return results
