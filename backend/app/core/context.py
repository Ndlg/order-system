from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUser:
    id: int
    username: str
    display_name: str
    role_names: tuple[str, ...]
    workspace_ids: tuple[int, ...]

    @property
    def is_system_admin(self) -> bool:
        return "system_admin" in self.role_names

    @property
    def can_write(self) -> bool:
        return "readonly" not in self.role_names

    def allowed_workspace_ids(self) -> set[int]:
        return set(self.workspace_ids)
