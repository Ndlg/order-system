from typing import Any

from fastapi import APIRouter, Body, HTTPException, Query, status

from app.services.memory_store import store


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

    @router.get("")
    def list_items(workspace_id: int | None = Query(default=None, ge=1)) -> list[dict[str, Any]]:
        return store.list_records(resource_name, workspace_id=workspace_id)

    @router.post("", status_code=status.HTTP_201_CREATED)
    def create_item(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
        return store.create_record(resource_name, payload)

    @router.get("/{record_id}")
    def get_item(record_id: int) -> dict[str, Any]:
        record = store.get_record(resource_name, record_id)
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{tag} record not found.")
        return record

    list_items.__name__ = f"list_{resource_name}"
    create_item.__name__ = f"create_{resource_name}"
    get_item.__name__ = f"get_{resource_name}"

    return router
