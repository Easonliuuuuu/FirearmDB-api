from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import joinedload
import schemas, models
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
router = APIRouter(prefix="/firearm", tags=["firearm"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[schemas.Firearm])
@limiter.limit("10/minute") # Apply the rate limit
def get_firearms(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Firearm).all()


@router.get("/{firearm_id}", response_model=schemas.Firearm)
def get_firearm(firearm_id: int, db: Session = Depends(get_db)):
    """
    Get a specific firearm by its ID.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.firearm_id == firearm_id).first()
    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    return db_firearm

@router.get("/search", response_model=List[schemas.Firearm])
def search_firearms(name: str, db: Session = Depends(get_db)):
    """
    Search for firearms by name (case-insensitive, partial match).
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    
    result = db.query(models.Firearm).filter(models.Firearm.name.ilike(f"%{name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="No firearms found matching the search criteria")
    return result

@router.get("/{firearm_id}/wars", response_model=List[schemas.War])
def get_wars_for_firearm(firearm_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all wars a specific firearm was used in.
    """
    db_firearm = db.query(models.Firearm).options(
        joinedload(models.Firearm.wars)
    ).filter(models.Firearm.firearm_id == firearm_id).first()

    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    return db_firearm.wars

@router.get("/{firearm_id}/cartridges", response_model=List[schemas.cartridge])
def get_cartridges_for_firearm(firearm_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all cartridges a specific firearm is chambered for.
    """
    db_firearm = db.query(models.Firearm).options(
        joinedload(models.Firearm.cartridges)
    ).filter(models.Firearm.firearm_id == firearm_id).first()

    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    return db_firearm.cartridges

@router.get("/{firearm_id}/manufacturers", response_model=List[schemas.manufacturer])
def get_manufacturers_for_firearm(firearm_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all manufacturers for a specific firearm.
    """
    db_firearm = db.query(models.Firearm).options(
        joinedload(models.Firearm.manufacturers)
    ).filter(models.Firearm.firearm_id == firearm_id).first()

    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    return db_firearm.manufacturers