from __future__ import annotations
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers import firearm, cartridge, firearm_type, war, manufacturer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import firearm, cartridge, war, auth as auth_router 
from app.auth import dynamic_key_func, try_get_current_user
from app.limiter import limiter
from app.context import _request_ctx_var 


app = FastAPI()

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    # Set the request context for each incoming request
    request_ctx = _request_ctx_var.set(request)
    response = await call_next(request)
    _request_ctx_var.reset(request_ctx)
    return response

@app.middleware("http")
async def add_user_to_state(request: Request, call_next):
    db: Session = next(get_db())
    try:
        user = await try_get_current_user(request, db)
        request.state.user = user
        if user:
            print(f"Authenticated request from user: {user.email}")
        else:
            print("Anonymous request")
    finally:
        db.close()
    
    response = await call_next(request)
    return response

app.state.limiter = limiter 
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(firearm.router, prefix="/api/v1")
app.include_router(cartridge.router, prefix="/api/v1")
app.include_router(war.router, prefix="/api/v1")
app.include_router(auth_router.router, prefix="/api/v1") 
app.include_router(manufacturer.router, prefix="/api/v1")
app.include_router(firearm_type.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


