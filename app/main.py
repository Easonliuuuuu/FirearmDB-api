from __future__ import annotations
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import firearm, cartridge, war, manufacturer, type
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from routers import firearm, cartridge, war, auth as auth_router # Import new router
import auth # Import auth for dependency
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.include_router(firearm.router)
app.include_router(cartridge.router)
app.include_router(war.router)
app.include_router(auth_router.router) 
app.include_router(manufacturer.router)
app.include_router(type.router)

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


