from models import RoleType
from schemas.base import UserBase


class UserOut(UserBase):
    id: str
    first_name: str
    last_name: str
    phone: str
    role: RoleType
    iban: str
