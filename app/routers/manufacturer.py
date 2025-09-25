from fastapi import APIRouter, Request
import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from database import get_db
from fastapi import Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import HTTPException
router = APIRouter(prefix="/manufacturer", tags=["manufacturer"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[schemas.manufacturer])
#@limiter.limit("5/minute") # Apply the rate limit
def get_manufacturers(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Manufacturer).all()

@router.get("/search", response_model=List[schemas.manufacturer])
def search_manufacturers(name: str, db: Session = Depends(get_db)):
    """
    Search for manufacturers by name (case-insensitive, partial match).
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    
    result = db.query(models.Manufacturer).filter(models.Manufacturer.name.ilike(f"%{name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="No manufacturers found matching the search criteria")
    return result

@router.get("/{manufacturer_id}", response_model=schemas.manufacturer)
def get_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    manufacturer = db.query(models.Manufacturer).filter(models.Manufacturer.manufacturer_id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer

@router.get("/{manufacturer_id}/firearms", response_model=List[schemas.Firearm])
#@limiter.limit("10/minute")
def get_firearms_for_manufacturer(request: Request, manufacturer_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms produced by a specific manufacturer.
    """
    # Use options(joinedload(...)) to perform an eager load of the firearms
    db_manufacturer = db.query(models.Manufacturer).options(
        joinedload(models.Manufacturer.firearms)
    ).filter(models.Manufacturer.manufacturer_id == manufacturer_id).first()

    if db_manufacturer is None:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    
    # The firearms are now pre-loaded with the manufacturer data.
    return db_manufacturer.firearms

@router.get("/{manufacturer_id}/firearms/names", response_model=List[schemas.NameWithManufacturer])
#@limiter.limit("10/minute")
def get_firearm_names_for_manufacturer(request: Request, manufacturer_id: int, db: Session = Depends(get_db)):
    """
    Get a list of firearm IDs and names produced by a specific manufacturer.
    """
    # Eagerly load the related firearms
    db_manufacturer = db.query(models.Manufacturer).options(
        joinedload(models.Manufacturer.firearms)
    ).filter(models.Manufacturer.manufacturer_id == manufacturer_id).first()

    if db_manufacturer is None:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    
    return db_manufacturer.firearms