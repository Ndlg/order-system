from typing import Any, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.base import Base


ModelT = TypeVar("ModelT", bound=Base)


class WorkspaceAccessError(PermissionError):
    pass


def model_to_dict(model: Base) -> dict[str, Any]:
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}


class Repository:
    def __init__(self, db: Session, model: type[ModelT]):
        self.db = db
        self.model = model

    @property
    def is_workspace_scoped(self) -> bool:
        return hasattr(self.model, "workspace_id")

    def _workspace_statement(self, workspace_id: int | None, allowed_workspace_ids: set[int]) -> Select[tuple[ModelT]]:
        statement = select(self.model).where(self.model.is_deleted.is_(False))
        if self.is_workspace_scoped:
            if workspace_id is None:
                statement = statement.where(self.model.workspace_id.in_(allowed_workspace_ids))
            else:
                if workspace_id not in allowed_workspace_ids:
                    raise WorkspaceAccessError("Workspace access denied.")
                statement = statement.where(self.model.workspace_id == workspace_id)
        return statement

    def list(
        self,
        *,
        workspace_id: int | None,
        allowed_workspace_ids: set[int],
        offset: int = 0,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        statement = self._workspace_statement(workspace_id, allowed_workspace_ids).offset(offset).limit(limit)
        return [model_to_dict(item) for item in self.db.scalars(statement).all()]

    def get(self, record_id: int, *, allowed_workspace_ids: set[int]) -> dict[str, Any] | None:
        statement = select(self.model).where(self.model.id == record_id, self.model.is_deleted.is_(False))
        if self.is_workspace_scoped:
            statement = statement.where(self.model.workspace_id.in_(allowed_workspace_ids))
        record = self.db.scalars(statement).first()
        return model_to_dict(record) if record else None

    def create(self, payload: dict[str, Any], *, workspace_id: int | None, user_id: int | None) -> dict[str, Any]:
        record_payload = dict(payload)
        if self.is_workspace_scoped:
            if workspace_id is None:
                raise WorkspaceAccessError("workspace_id is required.")
            record_payload["workspace_id"] = workspace_id
        record_payload.setdefault("created_by", user_id)
        record_payload.setdefault("updated_by", user_id)
        record = self.model(**record_payload)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return model_to_dict(record)

    def update(self, record_id: int, payload: dict[str, Any], *, allowed_workspace_ids: set[int], user_id: int | None) -> dict[str, Any] | None:
        statement = select(self.model).where(self.model.id == record_id, self.model.is_deleted.is_(False))
        if self.is_workspace_scoped:
            statement = statement.where(self.model.workspace_id.in_(allowed_workspace_ids))
        record = self.db.scalars(statement).first()
        if record is None:
            return None
        for key, value in payload.items():
            if key in {"id", "workspace_id", "created_at", "created_by"}:
                continue
            if hasattr(record, key):
                setattr(record, key, value)
        if hasattr(record, "updated_by"):
            record.updated_by = user_id
        self.db.commit()
        self.db.refresh(record)
        return model_to_dict(record)

    def soft_delete(self, record_id: int, *, allowed_workspace_ids: set[int], user_id: int | None) -> bool:
        statement = select(self.model).where(self.model.id == record_id, self.model.is_deleted.is_(False))
        if self.is_workspace_scoped:
            statement = statement.where(self.model.workspace_id.in_(allowed_workspace_ids))
        record = self.db.scalars(statement).first()
        if record is None:
            return False
        record.is_deleted = True
        if hasattr(record, "updated_by"):
            record.updated_by = user_id
        self.db.commit()
        return True
