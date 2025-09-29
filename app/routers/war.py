from fastapi import APIRouter, Request, HTTPException
from app import schemas, models
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from fastapi import Depends
from app.limiter import limiter
from app.auth import get_rate_limit
router = APIRouter(prefix="/war", tags=["war"])

@router.get("/", response_model=List[schemas.War])
@limiter.limit(get_rate_limit)
def get_firearms(db: Session = Depends(get_db)):
    return db.query(models.War).all()

@router.get("/search/", response_model=List[schemas.War])
def search_wars(request: Request, query: str, db: Session = Depends(get_db)):
    """
    Search for wars by name. The search is case-insensitive and matches partial text.
    """
    if not query:
        raise HTTPException(status_code=400, detail="A search query must be provided.")
    
    search_results = db.query(models.War).filter(models.War.name.ilike(f"%{query}%")).all()
    
    if not search_results:
        raise HTTPException(status_code=404, detail=f"No wars found matching '{query}'")
        
    return search_results

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