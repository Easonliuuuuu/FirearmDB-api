from fastapi import APIRouter, Request
from app import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from fastapi import Depends

from fastapi import HTTPException
router = APIRouter(prefix="/cartridge", tags=["cartridge"])

@router.get("/", response_model=List[schemas.cartridge])
def get_cartridges(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Cartridge).all()

@router.get("/search", response_model=List[schemas.cartridge])
def search_cartridges(name: str, db: Session = Depends(get_db)):
    """
    Search for cartridges by name (case-insensitive, partial match).
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    
    result = db.query(models.Cartridge).filter(models.Cartridge.name.ilike(f"%{name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="No cartridges found matching the search criteria")
    return result

@router.get("/{cartridge_id}", response_model=schemas.cartridge)
def get_cartridge(cartridge_id: int, db: Session = Depends(get_db)):
    cartridge = db.query(models.Cartridge).filter(models.Cartridge.cartridge_id == cartridge_id).first()
    if not cartridge:
        raise HTTPException(status_code=404, detail="Cartridge not found")
    return cartridge


@router.get("/{cartridge_id}/firearms", response_model=List[schemas.Firearm])
#@limiter.limit("10/minute")
def get_firearms_for_cartridge(request: Request, cartridge_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms that are chambered for a specific cartridge.
    """
    # Use options(joinedload(...)) to perform an eager load of the firearms
    db_cartridge = db.query(models.Cartridge).options(
        joinedload(models.Cartridge.firearms)
    ).filter(models.Cartridge.cartridge_id == cartridge_id).first()

    if db_cartridge is None:
        raise HTTPException(status_code=404, detail="Cartridge not found")
    
    # The firearms are now pre-loaded with the cartridge data.
    return db_cartridge.firearms



