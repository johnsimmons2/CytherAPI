from dataclasses import dataclass
from datetime import datetime

from api.model.dto.roleDto import RoleDTO


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    fName: str
    lName: str
    lastOnline: datetime
    created: datetime
    roles: list[RoleDTO]
