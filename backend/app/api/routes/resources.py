from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.context import CurrentUser
from app.core.database import get_db
from app.core.deps import get_current_user, get_workspace_id, require_write
from app.repositories.base import Repository, WorkspaceAccessError
from app.repositories.registry import RESOURCE_MODELS


RESOURCE_ROUTES = [
    ("/workspaces", "workspaces", "workspaces"),
    ("/users", "users", "users"),
    ("/roles", "roles", "roles"),
    ("/collectors", "collectors", "collectors"),
    ("/capture-tasks", "capture_tasks", "capture-tasks"),
    ("/capture-batches", "capture_batches", "capture-batches"),
    ("/raw-capture-records", "raw_capture_records", "raw-capture-records"),
    ("/waybill-modes", "waybill_modes", "waybill-modes"),
    ("/waybill-templates", "waybill_templates", "waybill-templates"),
    ("/standard-detail-batches", "standard_detail_batches", "standard-detail-batches"),
    ("/standard-details", "standard_details", "standard-details"),
    ("/field-definitions", "field_definitions", "field-definitions"),
    ("/field-role-configs", "field_role_configs", "field-role-configs"),
    ("/key-field-sets", "key_field_sets", "key-field-sets"),
    ("/match-rules", "match_rules", "match-rules"),
    ("/stalls", "stalls", "stalls"),
    ("/image-assets", "image_assets", "image-assets"),
    ("/report-batches", "report_batches", "report-batches"),
    ("/exceptions", "exception_records", "exceptions"),
    ("/export-records", "export_records", "export-records"),
]


def build_resource_router(resource_name: str, tag: str) -> APIRouter:
    router = APIRouter()
    model = RESOURCE_MODELS[resource_name]

    @router.get("")
    def list_items(
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user),
        workspace_id: int | None = Query(default=None, ge=1),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=100, ge=1, le=500),
    ) -> list[dict[str, Any]]:
        repo = Repository(db, model)
        try:
            records = repo.list(
                workspace_id=workspace_id,
                allowed_workspace_ids=current_user.allowed_workspace_ids(),
                offset=offset,
                limit=limit,
            )
            if resource_name == "workspaces" and not current_user.is_system_admin:
                allowed = current_user.allowed_workspace_ids()
                return [record for record in records if record["id"] in allowed]
            return records
        except WorkspaceAccessError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

    @router.post("", status_code=status.HTTP_201_CREATED)
    def create_item(
        payload: dict[str, Any] = Body(default_factory=dict),
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(require_write),
        workspace_id: int = Depends(get_workspace_id),
    ) -> dict[str, Any]:
        repo = Repository(db, model)
        try:
            return repo.create(payload, workspace_id=workspace_id, user_id=current_user.id)
        except WorkspaceAccessError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

    @router.get("/{record_id}")
    def get_item(
        record_id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user),
    ) -> dict[str, Any]:
        repo = Repository(db, model)
        record = repo.get(record_id, allowed_workspace_ids=current_user.allowed_workspace_ids())
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{tag} record not found.")
        if resource_name == "workspaces" and not current_user.is_system_admin and record["id"] not in current_user.allowed_workspace_ids():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Workspace access denied.")
        return record

    @router.patch("/{record_id}")
    def update_item(
        record_id: int,
        payload: dict[str, Any] = Body(default_factory=dict),
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(require_write),
    ) -> dict[str, Any]:
        repo = Repository(db, model)
        record = repo.update(
            record_id,
            payload,
            allowed_workspace_ids=current_user.allowed_workspace_ids(),
            user_id=current_user.id,
        )
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{tag} record not found.")
        return record

    @router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        record_id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(require_write),
    ) -> None:
        repo = Repository(db, model)
        deleted = repo.soft_delete(
            record_id,
            allowed_workspace_ids=current_user.allowed_workspace_ids(),
            user_id=current_user.id,
        )
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{tag} record not found.")

    list_items.__name__ = f"list_{resource_name}"
    create_item.__name__ = f"create_{resource_name}"
    get_item.__name__ = f"get_{resource_name}"

    return router
