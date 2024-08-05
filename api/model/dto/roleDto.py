from dataclasses import dataclass


@dataclass
class RoleDTO:
    id: int
    level: int
    roleName: str
