from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.context import CurrentUser
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import Role, User, UserWorkspace


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token.")
    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token.") from None

    user = db.get(User, user_id)
    if user is None or user.is_deleted or not user.is_enabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is disabled or missing.")

    memberships = db.execute(
        select(UserWorkspace, Role)
        .join(Role, Role.id == UserWorkspace.role_id, isouter=True)
        .where(UserWorkspace.user_id == user.id, UserWorkspace.is_deleted.is_(False))
    ).all()
    workspace_ids = tuple(sorted({user_workspace.workspace_id for user_workspace, _role in memberships}))
    role_names = tuple(sorted({role.name for _user_workspace, role in memberships if role is not None}))
    return CurrentUser(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        role_names=role_names,
        workspace_ids=workspace_ids,
    )


def get_workspace_id(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    x_workspace_id: Annotated[int | None, Header(alias="X-Workspace-Id")] = None,
) -> int:
    allowed = current_user.allowed_workspace_ids()
    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No workspace access.")
    workspace_id = x_workspace_id or min(allowed)
    if workspace_id not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Workspace access denied.")
    return workspace_id


def require_write(current_user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if not current_user.can_write:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Read-only users cannot write.")
    return current_user
