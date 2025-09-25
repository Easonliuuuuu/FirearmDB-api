from pydantic import BaseModel
from typing import Optional, List

#class userCreate(BaseModel):
    #email: str
    #password: str

class War(BaseModel):
    war_id: int
    name: str
    
    class Config:
        from_attributes = True
    
class cartridge(BaseModel):
    cartridge_id: int
    name: str

class Firearm(BaseModel):
    firearm_id: int
    name: str
    designer: Optional[str] = None
    designed: Optional[str] = None
    produced: Optional[str] = None
    action: Optional[str] = None
    #source_url: Optional[str] = None
    #image_url: Optional[str] = None
    wars: List[War] = []
    cartridges: List[cartridge] = []

    class Config:
        from_attributes = True

class manufacturer(BaseModel):
    manufacturer_id: int
    name: str

    class Config:
        from_attributes = True

class NameWithManufacturer(BaseModel):
    firearm_id: int
    name: str

    class Config:
        from_attributes = True
        

class NameWithCartridge(BaseModel):
    firearm_id: int
    name: str

    class Config:
        from_attributes = True
    
class NameWithType(BaseModel):
    firearm_id: int
    name: str

    class Config:
        from_attributes = True

class FirearmName(BaseModel):
    firearm_id: int
    name: str

    class Config:
        from_attributes = True

class type(BaseModel):
    type_id: int
    name: str

    class Config:
        from_attributes = True


    
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    #is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

