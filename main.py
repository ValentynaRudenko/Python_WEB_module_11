from fastapi import FastAPI, Depends, HTTPException, status, Security

from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.routes import contacts, auth
from src.database import models
from src.database.db import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
