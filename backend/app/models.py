from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Numeric, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    tin: Mapped[str | None] = mapped_column(String(64), nullable=True)
    properties = relationship("Property", back_populates="company", cascade="all, delete-orphan")

class Property(Base):
    __tablename__ = "property"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    company = relationship("Company", back_populates="properties")
    leases = relationship("Lease", back_populates="property", cascade="all, delete-orphan")

class Tenant(Base):
    __tablename__ = "tenant"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    leases = relationship("Lease", back_populates="tenant", cascade="all, delete-orphan")

class Lease(Base):
    __tablename__ = "lease"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id", ondelete="CASCADE"), nullable=False)
    from_date: Mapped[object] = mapped_column(Date, nullable=False)
    to_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    tenant = relationship("Tenant", back_populates="leases")
    property = relationship("Property", back_populates="leases")

class Rent(Base):
    __tablename__ = "rent"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id", ondelete="CASCADE"), nullable=False)
    from_date: Mapped[object] = mapped_column(Date, nullable=False)
    to_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    amount: Mapped[object] = mapped_column(Numeric(12,2), nullable=False)
    __table_args__ = (
        UniqueConstraint("property_id", "from_date", name="uq_rent_prop_from"),
        Index("ix_rent_prop", "property_id"),
    )

class AccountType(Base):
    __tablename__ = "account_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)  # e.g., ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

class AccountSubType(Base):
    __tablename__ = "account_sub_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("account_type.id", ondelete="RESTRICT"), nullable=False)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type = relationship("AccountType")

class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("account_type.id", ondelete="RESTRICT"), nullable=False)
    sub_type_id: Mapped[int | None] = mapped_column(ForeignKey("account_sub_type.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type = relationship("AccountType")
    sub_type = relationship("AccountSubType")

class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    debit_account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="RESTRICT"), nullable=False)
    credit_account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="RESTRICT"), nullable=False)
    property_id: Mapped[int | None] = mapped_column(ForeignKey("property.id", ondelete="SET NULL"), nullable=True)
    tenant_id: Mapped[int | None] = mapped_column(ForeignKey("tenant.id", ondelete="SET NULL"), nullable=True)
    date: Mapped[object] = mapped_column(Date, nullable=False)
    amount: Mapped[object] = mapped_column(Numeric(12,2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    __table_args__ = (
        Index("ix_trans_date", "date"),
        Index("ix_trans_property", "property_id"),
        Index("ix_trans_tenant", "tenant_id"),
    )
