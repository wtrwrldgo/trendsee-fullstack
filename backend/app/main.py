import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, publications, users, instagram
from .db import init_db

app = FastAPI(title="Trendsee Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(publications.router, prefix="/publications", tags=["publications"])
app.include_router(instagram.router, prefix="/instagram", tags=["instagram"])

@app.get("/")
async def root():
    return {"message": "Welcome to Trendsee API"}
