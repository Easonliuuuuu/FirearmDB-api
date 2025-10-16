from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class War(BaseModel):
    war_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Cartridge(BaseModel):
    cartridge_id: int
    name: str


class Firearm(BaseModel):
    firearm_id: int
    name: str
    designer: Optional[str] = None
    designed: Optional[str] = None
    produced: Optional[str] = None
    action: Optional[str] = None
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
    # is_active: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None