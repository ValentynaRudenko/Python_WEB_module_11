from fastapi import FastAPI, Depends, HTTPException, status, Security
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.lifespan import Lifespan

from sqlalchemy.orm import Session
from pydantic import BaseModel


from src.routes import contacts, auth, users
from src.database import models
from src.database.db import engine
from src.conf.config import settings


models.Base.metadata.create_all(bind=engine)


async def app_lifespan(app: FastAPI):
    print("Starting up...")
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0, encoding="utf-8",
        decode_responses=True
        )
    await FastAPILimiter.init(r)
    yield
    print("Shutting down...")

app = FastAPI(lifespan=app_lifespan)

origins = [
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}
