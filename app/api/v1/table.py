from fastapi import APIRouter, Depends
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import Table_Schema
from app.database.models import Table


router = APIRouter()

@router.get("/tables/")
def table_list(db: Session = Depends(get_db)):
    # список всех столиков
    return db.query(Table).all()

@router.post("/tables/")
def create_new_table(data: Table_Schema, db: Session = Depends(get_db)):
    # создать новый столик
    new_table = Table(
        name=data.name,
        seats=data.seats,
        location=data.location
    )
    db.add(new_table)
    db.commit()
    return {"message": "Success"}

@router.delete("/tables/{id}")
def delete_table(id, db: Session = Depends(get_db)):
    # удалить столик
    table = db.query(Table).filter(Table.id == int(id)).first()
    if table:
        db.delete(table)
        db.commit()
        return {"message": "The removal of the table was successful"}
    else:
        return {"Error": "There's no such table"}