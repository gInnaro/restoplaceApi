from fastapi import APIRouter, Depends
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import Reservation_Schema
from datetime import timedelta
import pytz
from app.database.models import Reservation, Table


router = APIRouter()

@router.get("/reservations/")
def all_reservations(db: Session = Depends(get_db)):
    # список всех броней
    return db.query(Reservation).all()

@router.post("/reservations/")
def create_new_reservations(data: Reservation_Schema, db: Session = Depends(get_db)):
    # создать новую бронь
    timezone_moscow = pytz.timezone('Europe/Moscow')

    if db.query(Table).filter(Table.id == data.table_id).first():
        reserved_table = db.query(Reservation).filter(Reservation.table_id == int(data.table_id)).all()
        for reserved in reserved_table:
            end_reserved_table = reserved.reservation_time + timedelta(minutes=int(reserved.duration_minutes))
            if timezone_moscow.localize(reserved.reservation_time) <= timezone_moscow.localize(data.reservation_time) <= timezone_moscow.localize(end_reserved_table):
                return {"Error": "A table cannot be reserved at this time"}

            end_reserved_time = timezone_moscow.localize(data.reservation_time + timedelta(minutes=data.duration_minutes))
            if timezone_moscow.localize(reserved.reservation_time) <= end_reserved_time <= timezone_moscow.localize(end_reserved_table):
                return {"Error": "A table cannot be reserved at this time"}

        new_reservations = Reservation(
            customer_name=data.customer_name,
            table_id=data.table_id,
            reservation_time=timezone_moscow.localize(data.reservation_time),
            duration_minutes=data.duration_minutes
        )
        db.add(new_reservations)
        db.commit()
        return {"message": "Success"}
    else:
        return {"Error": "There's no such table."}

@router.delete("/reservations/{id}")
def delete__reservations(id, db: Session = Depends(get_db)):
    # удалить бронь
    table = db.query(Reservation).filter(Reservation.id == int(id)).first()
    if table:
        db.delete(table)
        db.commit()
        return {"message": "The removal of the table reserve was successful."}
    else:
        return {"Error": "There is no such reserve"}