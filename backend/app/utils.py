from sqlalchemy.orm import Session
from sqlalchemy import func, select
from .models import Account, AccountType, Transaction

# Helper to compute balances based on account type normal balance rules
# Assets & Expenses: debit-normal (debits increase), so balance = debits - credits
# Liabilities, Equity, Revenue: credit-normal, so balance = credits - debits
def account_balance_query(as_of=None, start_date=None, end_date=None):
    # build base selectable for debit and credit sums per account
    debit_q = select(
        Transaction.debit_account_id.label("account_id"),
        func.sum(Transaction.amount).label("debit_sum"),
        func.cast(0, Transaction.amount.type).label("credit_sum")
    )
    credit_q = select(
        Transaction.credit_account_id.label("account_id"),
        func.cast(0, Transaction.amount.type).label("debit_sum"),
        func.sum(Transaction.amount).label("credit_sum")
    )
    # apply date filters
    def apply_dates(q):
        if as_of is not None:
            q = q.where(Transaction.date <= as_of)
        if start_date is not None:
            q = q.where(Transaction.date >= start_date)
        if end_date is not None:
            q = q.where(Transaction.date <= end_date)
        return q

    debit_q = apply_dates(debit_q).group_by(Transaction.debit_account_id)
    credit_q = apply_dates(credit_q).group_by(Transaction.credit_account_id)

    # union and aggregate
    from sqlalchemy import union_all
    unioned = union_all(debit_q, credit_q).subquery()
    from sqlalchemy import select as sel
    sums = sel(
        unioned.c.account_id,
        func.sum(unioned.c.debit_sum).label("debits"),
        func.sum(unioned.c.credit_sum).label("credits")
    ).group_by(unioned.c.account_id).subquery("sums")

    # join accounts and account types to compute signed balance
    acct = Account.__table__
    at = AccountType.__table__

    # CASE expression for sign
    from sqlalchemy import case
    balance_expr = case(
        (
            at.c.code.in_(["ASSET", "EXPENSE"]),
            sums.c.debits - sums.c.credits
        ),
        else_=sums.c.credits - sums.c.debits
    ).label("balance")

    return sel(
        sums.c.account_id,
        acct.c.name.label("account_name"),
        at.c.code.label("type_code"),
        balance_expr
    ).join(acct, acct.c.id == sums.c.account_id).join(at, at.c.id == acct.c.type_id)
