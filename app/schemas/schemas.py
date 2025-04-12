from pydantic import BaseModel
from datetime import datetime

class Table_Schema(BaseModel):
    name: str
    seats: int
    location: str


class Reservation_Schema(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int