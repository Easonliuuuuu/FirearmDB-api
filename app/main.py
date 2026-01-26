from __future__ import annotations
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routers import firearm, cartridge, firearm_type, war, manufacturer
from app.routers import auth as auth_router 
 
from mangum import Mangum


app = FastAPI()



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

handler = Mangum(app)


