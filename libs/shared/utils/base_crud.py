from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from libs.shared.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: Session):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[ModelType]:
        try:
            return (
                self.db.query(self.model).filter(self.model.id == id).first()
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during fetch: {str(e)}")

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        filter_type: str = "and",
    ) -> List[ModelType]:
        """
        Retrieve multiple objects with advanced filtering, skipping, and limiting.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 100.
            filters (Dict[str, Any], optional): Dictionary of column filters.
                Supports complex filtering with different conditions.
            filter_type (str, optional): Type of filter combination.
                Can be 'and' (default) or 'or'.

        Returns:
            List[ModelType]: List of database objects matching the filters.

        Raises:
            SQLAlchemyError: If there's an error during the database query.
            ValueError: If invalid filter type or column is provided.
        """
        try:
            query = self.db.query(self.model)

            if filters:
                if filter_type not in ["and", "or"]:
                    raise ValueError("Filter type must be 'and' or 'or'")

                filter_conditions = []
                for column, value in filters.items():
                    # Get the column from the model dynamically
                    model_column = getattr(self.model, column, None)

                    if model_column is None:
                        raise ValueError(
                            f"Column {column} does not exist in the model"
                        )

                    if value is None:
                        filter_conditions.append(model_column == None)
                    elif isinstance(value, dict):
                        for op, val in value.items():
                            if op == "eq":
                                filter_conditions.append(model_column == val)
                            elif op == "ne":
                                filter_conditions.append(model_column != val)
                            elif op == "gt":
                                filter_conditions.append(model_column > val)
                            elif op == "ge":
                                filter_conditions.append(model_column >= val)
                            elif op == "lt":
                                filter_conditions.append(model_column < val)
                            elif op == "le":
                                filter_conditions.append(model_column <= val)
                            elif op == "in":
                                filter_conditions.append(model_column.in_(val))
                            elif op == "like":
                                filter_conditions.append(
                                    model_column.like(val)
                                )
                            else:
                                raise ValueError(f"Unsupported operator: {op}")
                    elif isinstance(value, list):
                        filter_conditions.append(model_column.in_(value))
                    else:
                        filter_conditions.append(model_column == value)

                if filter_type == "and":
                    query = query.filter(and_(*filter_conditions))
                else: 
                    query = query.filter(or_(*filter_conditions))

            # Apply skip and limit
            return query.offset(skip).limit(limit).all()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during fetch: {str(e)}")

    def create(
        self, *, obj_in: CreateSchemaType, auto_commit: bool = False
    ) -> ModelType:

        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            self.db.add(db_obj)
            if auto_commit:
                self.db.commit()
                self.db.refresh(db_obj)
            else:
                self.db.flush()
            return db_obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during  creation: {str(e)}")

    def create_many(
        self, *, obj_list: List[CreateSchemaType], auto_commit: bool = False
    ) -> List[ModelType]:
        """
        Bulk create objects

        Args:
            obj_list: List of Pydantic models to create
        Returns:
            List of created database objects
        Raises:
            SQLAlchemyError: If there's an error during bulk creation
        """
        try:
            db_objs = []
            for obj in obj_list:
                obj_in_data = jsonable_encoder(obj)
                db_obj = self.model(**obj_in_data)
                self.db.add(db_obj)
                db_objs.append(db_obj)

            if auto_commit:
                self.db.commit()
                for db_obj in db_objs:
                    self.db.refresh(db_obj)
            else:
                self.db.flush()

            return db_objs

        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during bulk creation: {str(e)}")

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        auto_commit: bool = False,
    ) -> ModelType:

        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            self.db.add(db_obj)

            if auto_commit:
                self.db.commit()
                self.db.refresh(db_obj)
            else:
                self.db.flush()
            return db_obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during update: {str(e)}")

    def remove(self, *, id: int, auto_commit: bool = False) -> ModelType:
        try:
            obj = self.db.query(self.model).get(id)
            self.db.delete(obj)
            if auto_commit:
                self.db.commit()
            else:
                self.db.flush()

            return obj

        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error during deletion: {str(e)}")
