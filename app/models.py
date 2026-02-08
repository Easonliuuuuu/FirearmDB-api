from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base 
from pydantic import BaseModel
from typing import Optional, List
# --- Junction Tables (Association Tables) ---
# These tables don't need their own class. They are defined here to be used
# in the 'secondary' argument of the relationships below.

firearm_types = Table('firearm_types', Base.metadata,
    Column('firearm_id', Integer, ForeignKey('firearms.firearm_id'), primary_key=True),
    Column('type_id', Integer, ForeignKey('types.type_id'), primary_key=True)
)

firearm_wars = Table('firearm_wars', Base.metadata,
    Column('firearm_id', Integer, ForeignKey('firearms.firearm_id'), primary_key=True),
    Column('war_id', Integer, ForeignKey('wars.war_id'), primary_key=True)
)

firearm_cartridges = Table('firearm_cartridges', Base.metadata,
    Column('firearm_id', Integer, ForeignKey('firearms.firearm_id'), primary_key=True),
    Column('cartridge_id', Integer, ForeignKey('cartridges.cartridge_id'), primary_key=True)
)

firearm_manufacturers = Table('firearm_manufacturers', Base.metadata,
    Column('firearm_id', Integer, ForeignKey('firearms.firearm_id'), primary_key=True),
    Column('manufacturer_id', Integer, ForeignKey('manufacturers.manufacturer_id'), primary_key=True)
)

firearm_variants = Table('firearm_variants', Base.metadata,
    Column('firearm_id', Integer, ForeignKey('firearms.firearm_id'), primary_key=True),
    Column('variant_id', Integer, ForeignKey('variants.variant_id'), primary_key=True)
)


# --- Main Firearm Table Model ---

class Firearm(Base):
    __tablename__ = "firearms"

    firearm_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    designer = Column(Text)
    designed = Column(String(255))
    produced = Column(Text)
    action = Column(Text)
    

    # Many-to-Many relationships defined using the junction tables
    types = relationship("Type", secondary=firearm_types, back_populates="firearms")
    wars = relationship("War", secondary=firearm_wars, back_populates="firearms")
    cartridges = relationship("Cartridge", secondary=firearm_cartridges, back_populates="firearms")
    manufacturers = relationship("Manufacturer", secondary=firearm_manufacturers, back_populates="firearms")
    variants = relationship("Variant", secondary=firearm_variants, back_populates="firearms")


# --- Lookup Table Models ---

class Type(Base):
    __tablename__ = "types"
    type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    firearms = relationship("Firearm", secondary=firearm_types, back_populates="types")

class War(Base):
    __tablename__ = "wars"
    war_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    firearms = relationship("Firearm", secondary=firearm_wars, back_populates="wars")

class Cartridge(Base):
    __tablename__ = "cartridges"
    cartridge_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    firearms = relationship("Firearm", secondary=firearm_cartridges, back_populates="cartridges")

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    manufacturer_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    firearms = relationship("Firearm", secondary=firearm_manufacturers, back_populates="manufacturers")

class Variant(Base):
    __tablename__ = "variants"
    variant_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    firearms = relationship("Firearm", secondary=firearm_variants, back_populates="variants")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

