from typing import Any, Dict, Generic, Optional, TypeVar, Union, List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == id).first()

    def get_uuid(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == str(id)).first()

    def get_form_id(self, db: Session, user_id: str, form_id: str) -> Optional[ModelType]:
        return db.query(self.model).filter_by(user_id=user_id, form_id=str(form_id)).first()

    def get_user_id(self, db: Session, user_id: str) -> Optional[ModelType]:
        return db.query(self.model).filter_by(user_id=user_id, second_stage=False).first()

    def get_multi(self, db: Session, *, create_user: str , offset: int = 0, limit: int = 1000, order: Column = None
                  ) -> list[tuple[ModelType]]:
        if order:
            return db.query(self.model).filter_by(create_user=create_user).order_by(order).offset(offset * limit).limit(limit).all()
        else:
            return db.query(self.model).filter_by(create_user=create_user).offset(offset * limit).limit(limit).all()



    def get_all(self, db: Session) -> list[tuple[ModelType]]:
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_bulk(self, db: Session, *, obj_in: List[CreateSchemaType]) -> List[ModelType]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj_list = list(
            map(
                lambda x: self.model(**x),
                obj_in_data,
            )
        )

        db.add_all(db_obj_list)
        db.commit()
        for obj in db_obj_list:
            db.refresh(obj)
        return db_obj_list

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
            else:
                setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def delete(self, db: Session, *, uuid: str) -> ModelType:
        obj = self.get_uuid(db, uuid)
        db.delete(obj)
        db.commit()
        return obj

    def deactivate(self, db: Session, *, uuid: str) -> ModelType:
        obj = self.get_uuid(db, uuid)
        obj.status = not obj.status
        db.commit()
        return obj

