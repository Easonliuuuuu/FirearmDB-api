from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import schemas, models, auth
from app.database import get_db
from typing import List

router = APIRouter(prefix="/firearm", tags=["Firearm"])

@router.get("/")
def get_firearms(
    offset: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """Get all firearms with pagination. Default limit=50, max limit=200."""
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    total = db.query(models.Firearm).count()
    items = db.query(models.Firearm).offset(offset).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/search")
def search_firearms(
    name: str, 
    offset: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """Search for firearms by name with pagination."""
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    query = db.query(models.Firearm).filter(models.Firearm.name.ilike(f"%{name}%"))
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    if total == 0:
        raise HTTPException(status_code=404, detail="No firearms found matching the search criteria")
    
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/{firearm_id}", response_model=schemas.Firearm)
def get_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a specific firearm by its ID.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.firearm_id == firearm_id).first()
    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    return db_firearm



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

@router.get("/{firearm_id}/cartridges", response_model=List[schemas.Cartridge])
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

@router.get("/{firearm_id}/manufacturers", response_model=List[schemas.Manufacturer])
def get_manufacturers_for_firearm(firearm_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a list of all manufacturers for a specific firearm.
    """
    db_firearm = db.query(models.Firearm).options(
        joinedload(models.Firearm.manufacturers)
    ).filter(models.Firearm.firearm_id == firearm_id).first()

    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    

@router.post("/", response_model=schemas.Firearm, status_code=status.HTTP_201_CREATED)
def create_firearm(firearm: schemas.FirearmCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    """
    Create a new firearm. Requires Admin privileges.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.name == firearm.name).first()
    if db_firearm:
        raise HTTPException(status_code=400, detail="Firearm with this name already exists")
    
    new_firearm = models.Firearm(**firearm.model_dump())
    db.add(new_firearm)
    db.commit()
    db.refresh(new_firearm)
    return new_firearm

@router.put("/{firearm_id}", response_model=schemas.Firearm)
def update_firearm(firearm_id: int, firearm: schemas.FirearmUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    """
    Update a firearm's details. Requires Admin privileges.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.firearm_id == firearm_id).first()
    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    # Update fields
    update_data = firearm.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_firearm, key, value)
    
    db.commit()
    db.refresh(db_firearm)
    return db_firearm

@router.delete("/{firearm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_firearm(firearm_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    """
    Delete a firearm. Requires Admin privileges.
    """
    db_firearm = db.query(models.Firearm).filter(models.Firearm.firearm_id == firearm_id).first()
    if db_firearm is None:
        raise HTTPException(status_code=404, detail="Firearm not found")
    
    db.delete(db_firearm)
    db.commit()
    return None
