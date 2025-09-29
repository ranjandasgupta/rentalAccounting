from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas
from ..crud import CRUD

router = APIRouter(prefix="/api", tags=["basic"])

crud_company = CRUD(models.Company)
crud_property = CRUD(models.Property)
crud_tenant = CRUD(models.Tenant)
crud_lease = CRUD(models.Lease)
crud_rent = CRUD(models.Rent)

# Company
@router.get("/companies", response_model=List[schemas.CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return crud_company.list(db)

@router.post("/companies", response_model=schemas.CompanyRead)
def create_company(body: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud_company.create(db, body.model_dump())

# Property
@router.get("/properties", response_model=List[schemas.PropertyRead])
def list_properties(db: Session = Depends(get_db)):
    return crud_property.list(db)

@router.post("/properties", response_model=schemas.PropertyRead)
def create_property(body: schemas.PropertyCreate, db: Session = Depends(get_db)):
    return crud_property.create(db, body.model_dump())

# Tenant
@router.get("/tenants", response_model=List[schemas.TenantRead])
def list_tenants(db: Session = Depends(get_db)):
    return crud_tenant.list(db)

@router.post("/tenants", response_model=schemas.TenantRead)
def create_tenant(body: schemas.TenantCreate, db: Session = Depends(get_db)):
    return crud_tenant.create(db, body.model_dump())

# Lease
@router.get("/leases", response_model=List[schemas.LeaseRead])
def list_leases(db: Session = Depends(get_db)):
    return crud_lease.list(db)

@router.post("/leases", response_model=schemas.LeaseRead)
def create_lease(body: schemas.LeaseCreate, db: Session = Depends(get_db)):
    return crud_lease.create(db, body.model_dump())

# Rent
@router.get("/rents", response_model=List[schemas.RentRead])
def list_rents(db: Session = Depends(get_db)):
    return crud_rent.list(db)

@router.post("/rents", response_model=schemas.RentRead)
def create_rent(body: schemas.RentCreate, db: Session = Depends(get_db)):
    return crud_rent.create(db, body.model_dump())
