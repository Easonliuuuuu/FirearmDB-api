from fastapi import APIRouter, Request
from app import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from fastapi import Depends
from app.limiter import limiter
from app.auth import get_rate_limit
from fastapi import HTTPException
router = APIRouter(prefix="/type", tags=["type"])

@router.get("/", response_model=List[schemas.type])
@limiter.limit(get_rate_limit)
def get_types(request: Request, db: Session = Depends(get_db)):
    return db.query(models.Type).all()

@router.get("/search", response_model=List[schemas.type])
def search_types(name: str, db: Session = Depends(get_db)):
    """
    Search for types by name (case-insensitive, partial match).
    """
    if not name:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    
    result = db.query(models.Type).filter(models.Type.name.ilike(f"%{name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="No types found matching the search criteria")
    return result

@router.get("/{type_id}", response_model=schemas.type)
def get_type(type_id: int, db: Session = Depends(get_db)):
    type_instance = db.query(models.Type).filter(models.Type.type_id == type_id).first()
    if not type_instance:
        raise HTTPException(status_code=404, detail="Type not found")
    return type_instance

@router.get("/{type_id}/firearms", response_model=List[schemas.Firearm])
def get_firearms_for_type(request: Request, type_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms of a specific type.
    """
    db_type = db.query(models.Type).options(
        joinedload(models.Type.firearms)
    ).filter(models.Type.type_id == type_id).first()

    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    
    return db_type.firearms

@router.get("/{type_id}/firearms/names", response_model=List[schemas.NameWithType])
def get_firearm_names_for_type(request: Request, type_id: int, db: Session = Depends(get_db)):
    """
    Get a list of firearm IDs and names of a specific type.
    """
    db_type = db.query(models.Type).options(
        joinedload(models.Type.firearms)
    ).filter(models.Type.type_id == type_id).first()

    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    
    return [schemas.NameWithType(firearm_id=firearm.firearm_id, name=firearm.name) for firearm in db_type.firearms]