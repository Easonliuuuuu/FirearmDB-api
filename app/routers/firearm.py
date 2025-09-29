from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app import schemas, models
from app.database import get_db
from typing import List

from app.limiter import limiter
from app.auth import get_rate_limit, is_user_exempt

router = APIRouter(prefix="/firearm", tags=["firearm"])

@router.get("/", response_model=List[schemas.Firearm])
@limiter.limit(get_rate_limit)
def get_firearms(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Firearm).all()

@router.get("/{firearm_id}", response_model=schemas.Firearm)
def get_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a specific firearm by its ID.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.firearm_id == firearm_id).first()
    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    return db_firearm

@router.get("/search", response_model=List[schemas.Firearm])
def search_firearms(name: str, request: Request, db: Session = Depends(get_db)):
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
def get_wars_for_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
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
def get_cartridges_for_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
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
def get_manufacturers_for_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a list of all manufacturers for a specific firearm.
    """
    db_firearm = db.query(models.Firearm).options(
        joinedload(models.Firearm.manufacturers)
    ).filter(models.Firearm.firearm_id == firearm_id).first()

    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    return db_firearm.manufacturers