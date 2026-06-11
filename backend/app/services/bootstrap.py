from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import Role, User, UserWorkspace, WaybillMode, Workspace


def seed_initial_data(db: Session) -> None:
    workspace = db.scalars(select(Workspace).where(Workspace.code == "default")).first()
    if workspace is None:
        workspace = Workspace(name="Default workspace", code="default", remark="Initial workspace.")
        db.add(workspace)
        db.flush()

    role = db.scalars(
        select(Role).where(Role.workspace_id == workspace.id, Role.name == "system_admin")
    ).first()
    if role is None:
        role = Role(workspace_id=workspace.id, name="system_admin", remark="System administrator.")
        db.add(role)
        db.flush()

    user = db.scalars(select(User).where(User.username == "admin")).first()
    if user is None:
        user = User(
            username="admin",
            display_name="Administrator",
            password_hash=hash_password("admin123"),
            is_enabled=True,
        )
        db.add(user)
        db.flush()

    membership = db.scalars(
        select(UserWorkspace).where(
            UserWorkspace.workspace_id == workspace.id,
            UserWorkspace.user_id == user.id,
        )
    ).first()
    if membership is None:
        db.add(UserWorkspace(workspace_id=workspace.id, user_id=user.id, role_id=role.id))

    waybill_mode = db.scalars(
        select(WaybillMode).where(
            WaybillMode.workspace_id == workspace.id,
            WaybillMode.code == "manual_upload",
        )
    ).first()
    if waybill_mode is None:
        db.add(
            WaybillMode(
                workspace_id=workspace.id,
                name="Manual upload",
                code="manual_upload",
                input_format="excel_row",
                remark="Initial mode for uploaded spreadsheets.",
                is_enabled=True,
            )
        )

    db.commit()
