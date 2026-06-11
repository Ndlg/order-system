import os
from pathlib import Path


TEST_DB = Path(__file__).resolve().parent / "foundation_test.db"
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"
os.environ["AUTO_CREATE_TABLES"] = "true"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_auth_and_workspace_scoped_field_definition_flow() -> None:
    with TestClient(app) as client:
        login = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "X-Workspace-Id": "1"}

        me = client.get("/api/v1/auth/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["username"] == "admin"
        assert me.json()["workspaces"][0]["id"] == 1

        created = client.post(
            "/api/v1/field-definitions",
            headers=headers,
            json={"name": "Field A", "code": "field_a", "data_type": "text"},
        )
        assert created.status_code == 201
        assert created.json()["workspace_id"] == 1

        records = client.get("/api/v1/field-definitions", headers=headers)
        assert records.status_code == 200
        assert len(records.json()) == 1


def teardown_module() -> None:
    from app.core.database import engine

    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()
