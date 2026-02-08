from fastapi import APIRouter, Request
from app import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from fastapi import Depends, HTTPException
router = APIRouter(prefix="/cartridge", tags=["Cartridge"])

@router.get("/")
def get_cartridges(
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all cartridges with pagination. Default limit=50, max limit=200."""
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    total = db.query(models.Cartridge).count()
    items = db.query(models.Cartridge).offset(offset).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/search")
def search_cartridges(
    name: str,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Search for cartridges by name with pagination."""
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    query = db.query(models.Cartridge).filter(models.Cartridge.name.ilike(f"%{name}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    if total == 0:
        raise HTTPException(status_code=404, detail="No cartridges found matching the search criteria")
    
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/{cartridge_id}", response_model=schemas.Cartridge)
def get_cartridge(cartridge_id: int, db: Session = Depends(get_db)):
    cartridge = db.query(models.Cartridge).filter(models.Cartridge.cartridge_id == cartridge_id).first()
    if not cartridge:
        raise HTTPException(status_code=404, detail="Cartridge not found")
    return cartridge


@router.get("/{cartridge_id}/firearms", response_model=List[schemas.Firearm])
def get_firearms_for_cartridge(cartridge_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms that are chambered for a specific cartridge.
    """
    
    db_cartridge = db.query(models.Cartridge).options(
        joinedload(models.Cartridge.firearms)
    ).filter(models.Cartridge.cartridge_id == cartridge_id).first()

    if db_cartridge is None:
        raise HTTPException(status_code=404, detail="Cartridge not found")
    
    return db_cartridge.firearms

@router.get("/{cartridge_id}/firearms/names", response_model=List[schemas.NameWithCartridge])
def get_firearm_names_for_cartridge(request: Request, cartridge_id: int, db: Session = Depends(get_db)):
    """
    Get a list of firearm IDs and names that are chambered for a specific cartridge.
    """
    db_cartridge = db.query(models.Cartridge).options(
        joinedload(models.Cartridge.firearms)
    ).filter(models.Cartridge.cartridge_id == cartridge_id).first()

    if db_cartridge is None:
        raise HTTPException(status_code=404, detail="Cartridge not found")
    
    return [
        schemas.NameWithManufacturer(
            firearm_id=firearm.firearm_id, 
            name=firearm.name,
            manufacturer=firearm.manufacturer.name if firearm.manufacturer else None
        ) 
        for firearm in db_cartridge.firearms
    ]





