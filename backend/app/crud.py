from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List, Optional
from .database import Base
from sqlalchemy import select
T = TypeVar("T", bound=Base)

class CRUD(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[T]:
        return db.get(self.model, id)

    def list(self, db: Session, limit: int = 100, offset: int = 0) -> List[T]:
        return db.scalars(select(self.model).offset(offset).limit(limit)).all()

    def create(self, db: Session, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, obj_in: dict) -> Optional[T]:
        obj = self.get(db, id)
        if not obj:
            return None
        for k, v in obj_in.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
