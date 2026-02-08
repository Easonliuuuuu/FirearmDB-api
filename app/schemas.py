from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Generic, TypeVar

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper."""
    items: List[T]
    total: int
    offset: int
    limit: int
    has_more: bool


class War(BaseModel):
    war_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Cartridge(BaseModel):
    cartridge_id: int
    name: str



class FirearmBase(BaseModel):
    name: str
    designer: Optional[str] = None
    designed: Optional[str] = None
    produced: Optional[str] = None
    action: Optional[str] = None

class FirearmCreate(FirearmBase):
    pass

class FirearmUpdate(FirearmBase):
    name: Optional[str] = None

class Firearm(FirearmBase):
    firearm_id: int
    wars: List[War] = []
    cartridges: List[Cartridge] = []

    model_config = ConfigDict(from_attributes=True)



class Manufacturer(BaseModel):
    manufacturer_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NameWithManufacturer(BaseModel):
    firearm_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NameWithCartridge(BaseModel):
    firearm_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NameWithType(BaseModel):
    firearm_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class FirearmName(BaseModel):
    firearm_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Type(BaseModel):
    type_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None