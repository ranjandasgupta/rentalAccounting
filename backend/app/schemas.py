from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# --- Basic Tables ---
class CompanyBase(BaseModel):
    name: str
    tin: Optional[str] = None

class CompanyCreate(CompanyBase): pass

class CompanyRead(CompanyBase):
    id: int
    class Config: from_attributes = True

class PropertyBase(BaseModel):
    company_id: int
    address: str
    description: Optional[str] = None

class PropertyCreate(PropertyBase): pass

class PropertyRead(PropertyBase):
    id: int
    class Config: from_attributes = True

class TenantBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class TenantCreate(TenantBase): pass

class TenantRead(TenantBase):
    id: int
    class Config: from_attributes = True

class LeaseBase(BaseModel):
    tenant_id: int
    property_id: int
    from_date: date
    to_date: Optional[date] = None

class LeaseCreate(LeaseBase): pass

class LeaseRead(LeaseBase):
    id: int
    class Config: from_attributes = True

class RentBase(BaseModel):
    property_id: int
    from_date: date
    to_date: Optional[date] = None
    amount: float

class RentCreate(RentBase): pass

class RentRead(RentBase):
    id: int
    class Config: from_attributes = True

# --- Accounting ---
class AccountTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class AccountTypeCreate(AccountTypeBase): pass

class AccountTypeRead(AccountTypeBase):
    id: int
    class Config: from_attributes = True

class AccountSubTypeBase(BaseModel):
    type_id: int
    code: str
    name: str
    description: Optional[str] = None

class AccountSubTypeCreate(AccountSubTypeBase): pass

class AccountSubTypeRead(AccountSubTypeBase):
    id: int
    class Config: from_attributes = True

class AccountBase(BaseModel):
    type_id: int
    sub_type_id: Optional[int] = None
    name: str
    description: Optional[str] = None

class AccountCreate(AccountBase): pass

class AccountRead(AccountBase):
    id: int
    class Config: from_attributes = True

class TransactionBase(BaseModel):
    debit_account_id: int
    credit_account_id: int
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None
    date: date
    amount: float
    description: Optional[str] = None

class TransactionCreate(TransactionBase): pass

class TransactionRead(TransactionBase):
    id: int
    class Config: from_attributes = True

# --- Reports ---
class IncomeStatementLine(BaseModel):
    account_id: int
    account_name: str
    amount: float

class IncomeStatement(BaseModel):
    start_date: date
    end_date: date
    revenue: List[IncomeStatementLine]
    expenses: List[IncomeStatementLine]
    total_revenue: float
    total_expenses: float
    net_income: float

class BalanceSheetSectionLine(BaseModel):
    account_id: int
    account_name: str
    amount: float

class BalanceSheet(BaseModel):
    as_of: date
    assets: List[BalanceSheetSectionLine]
    liabilities: List[BalanceSheetSectionLine]
    equity: List[BalanceSheetSectionLine]
    total_assets: float
    total_liabilities: float
    total_equity: float

class ExpenseReportLine(BaseModel):
    account_id: int
    account_name: str
    amount: float
    property_id: Optional[int] = None
    tenant_id: Optional[int] = None

class ExpenseReport(BaseModel):
    start_date: date
    end_date: date
    lines: List[ExpenseReportLine]
    total_expenses: float

class AuditResult(BaseModel):
    check: str
    passed: bool
    details: Optional[str] = None
