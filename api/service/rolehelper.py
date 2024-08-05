from api.model.dto.roleDto import RoleDTO
from api.model.dto.userDto import UserDTO
from api.service.dbservice import UserService
from api.service.jwthelper import get_access_token, decode_token


def get_userdto_from_token() -> UserDTO | None:
    try:
      token = decode_token(get_access_token())
      user = UserService.getByUsername(token['username'])

      userDTO = UserDTO()
      userDTO.id = user.id
      userDTO.username = user.username
      userDTO.email = user.email
      userDTO.fName = user.fName
      userDTO.lName = user.lName
      userDTO.lastOnline = user.lastOnline
      userDTO.created = user.created
      userDTO.roles = []

      for role in user.roles:
          roleDTO = RoleDTO()
          roleDTO.roleName = role.roleName
          roleDTO.level = role.level
          userDTO.roles.append(roleDTO)

      return userDTO
    except:
      return None
