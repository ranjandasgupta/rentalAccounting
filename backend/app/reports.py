from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from .models import Account, AccountType, Transaction
from .utils import account_balance_query

def income_statement(db: Session, start_date: date, end_date: date):
    q = account_balance_query(start_date=start_date, end_date=end_date)
    rows = db.execute(q).all()

    revenue = []
    expenses = []
    total_rev = 0.0
    total_exp = 0.0
    for account_id, account_name, type_code, balance in rows:
        amt = float(balance or 0)
        if type_code == "REVENUE":
            revenue.append({"account_id": account_id, "account_name": account_name, "amount": amt})
            total_rev += amt
        elif type_code == "EXPENSE":
            # for expenses, amounts should be positive in the report
            expenses.append({"account_id": account_id, "account_name": account_name, "amount": abs(amt)})
            total_exp += abs(amt)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "revenue": revenue,
        "expenses": expenses,
        "total_revenue": total_rev,
        "total_expenses": total_exp,
        "net_income": total_rev - total_exp,
    }

def balance_sheet(db: Session, as_of: date):
    q = account_balance_query(as_of=as_of)
    rows = db.execute(q).all()

    assets, liabilities, equity = [], [], []
    ta = tl = te = 0.0

    for account_id, account_name, type_code, balance in rows:
        amt = float(balance or 0)
        if type_code == "ASSET":
            assets.append({"account_id": account_id, "account_name": account_name, "amount": amt})
            ta += amt
        elif type_code == "LIABILITY":
            liabilities.append({"account_id": account_id, "account_name": account_name, "amount": amt})
            tl += amt
        elif type_code == "EQUITY":
            equity.append({"account_id": account_id, "account_name": account_name, "amount": amt})
            te += amt

    return {
        "as_of": as_of,
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "total_assets": ta,
        "total_liabilities": tl,
        "total_equity": te,
    }

def expense_report(db: Session, start_date: date, end_date: date):
    # Aggregate expense accounts by account (and optionally property/tenant)
    from sqlalchemy import func, case
    at = AccountType.__table__
    a = Account.__table__
    t = Transaction.__table__

    # Join to filter expense accounts
    expense_accounts = (
        select(
            a.c.id.label("account_id"),
            a.c.name.label("account_name"),
            t.c.property_id,
            t.c.tenant_id,
            func.sum(
                case((t.c.debit_account_id == a.c.id, t.c.amount), else_=0)
                - case((t.c.credit_account_id == a.c.id, t.c.amount), else_=0)
            ).label("amount")
        )
        .join(at, at.c.id == a.c.type_id)
        .join(t, (t.c.debit_account_id == a.c.id) | (t.c.credit_account_id == a.c.id))
        .where(at.c.code == "EXPENSE")
        .where(t.c.date >= start_date, t.c.date <= end_date)
        .group_by(a.c.id, a.c.name, t.c.property_id, t.c.tenant_id)
    )
    rows = db.execute(expense_accounts).all()
    lines = []
    total = 0.0
    for account_id, account_name, property_id, tenant_id, amt in rows:
        val = abs(float(amt or 0))
        lines.append({
            "account_id": account_id,
            "account_name": account_name,
            "property_id": property_id,
            "tenant_id": tenant_id,
            "amount": val
        })
        total += val
    return {
        "start_date": start_date,
        "end_date": end_date,
        "lines": lines,
        "total_expenses": total
    }
