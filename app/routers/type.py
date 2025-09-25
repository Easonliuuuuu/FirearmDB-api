from fastapi import APIRouter, Request
import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from database import get_db
from fastapi import Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import HTTPException
router = APIRouter(prefix="/type", tags=["type"])
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[schemas.type])
@limiter.limit("5/minute") # Apply the rate limit
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
#@limiter.limit("10/minute")
def get_firearms_for_type(request: Request, type_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms of a specific type.
    """
    # Use options(joinedload(...)) to perform an eager load of the firearms
    db_type = db.query(models.Type).options(
        joinedload(models.Type.firearms)
    ).filter(models.Type.type_id == type_id).first()

    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    
    # The firearms are now pre-loaded with the type data.
    return db_type.firearms

@router.get("/{type_id}/firearms/names", response_model=List[schemas.NameWithType])
#@limiter.limit("10/minute")
def get_firearm_names_for_type(request: Request, type_id: int, db: Session = Depends(get_db)):
    """
    Get a list of firearm IDs and names of a specific type.
    """
    # Use options(joinedload(...)) to perform an eager load of the firearms
    db_type = db.query(models.Type).options(
        joinedload(models.Type.firearms)
    ).filter(models.Type.type_id == type_id).first()

    if db_type is None:
        raise HTTPException(status_code=404, detail="Type not found")
    
    # The firearms are now pre-loaded with the type data.
    return [schemas.NameWithType(firearm_id=firearm.firearm_id, name=firearm.name) for firearm in db_type.firearms]