from fastapi import FastAPI
from app.api.v1 import table, reservation
from app.database.models import Base
from app.database.database import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(table.router)
app.include_router(reservation.router)

@app.get("/")
def root():
    return {"message": "Hello to RestoplaceApi"}

