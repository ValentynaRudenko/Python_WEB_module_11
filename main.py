from fastapi import FastAPI
from src.routes import contacts
from src.database import models
from src.database.db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}
