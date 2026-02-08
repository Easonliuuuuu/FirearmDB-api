from fastapi import APIRouter, Request, HTTPException
from app import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from fastapi import Depends
router = APIRouter(prefix="/war", tags=["War"])

@router.get("/")
def get_wars(
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all wars with pagination. Default limit=50, max limit=200."""
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    total = db.query(models.War).count()
    items = db.query(models.War).offset(offset).limit(limit).all()
    
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/search/")
def search_wars(
    query: str,
    offset: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Search for wars by name with pagination."""
    if not query:
        raise HTTPException(status_code=400, detail="A search query must be provided.")
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0
    
    q = db.query(models.War).filter(models.War.name.ilike(f"%{query}%"))
    total = q.count()
    items = q.offset(offset).limit(limit).all()
    
    if total == 0:
        raise HTTPException(status_code=404, detail=f"No wars found matching '{query}'")
        
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total
    }

@router.get("/{war_id}", response_model=schemas.War)
def get_war_by_id(request: Request, war_id: int, db: Session = Depends(get_db)):
    """
    Get details for a specific war by its ID.
    """
    db_war = db.query(models.War).filter(models.War.war_id == war_id).first()
    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    return db_war

@router.get("/{war_id}/firearms", response_model=List[schemas.Firearm])
def get_firearms_for_war(request: Request, war_id: int, db: Session = Depends(get_db)):
    """
    Get a list of all firearms used in a specific war.
    """
    # Eagerly load the related firearms to avoid session closing issues
    db_war = db.query(models.War).options(
        joinedload(models.War.firearms)
    ).filter(models.War.war_id == war_id).first()

    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    
    return db_war.firearms

@router.get("/{war_id}/firearms/names", response_model=List[schemas.FirearmName])
def get_firearm_names_for_war(request: Request, war_id: int, db: Session = Depends(get_db)):
    """
    Get a list of firearm IDs and names used in a specific war.
    """
    # Eagerly load the related firearms
    db_war = db.query(models.War).options(
        joinedload(models.War.firearms)
    ).filter(models.War.war_id == war_id).first()

    if db_war is None:
        raise HTTPException(status_code=404, detail="War not found")
    
    # Return the full firearm objects; FastAPI will serialize them using the FirearmName schema
    return db_war.firearms