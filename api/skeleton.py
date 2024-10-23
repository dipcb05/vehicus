#maintaining input skeleton model

from pydantic import BaseModel
from typing import Optional

class AllocationCreate(BaseModel):
    employee_id: str
    vehicle_id: str
    allocation_date: str

class AllocationUpdate(BaseModel):
    employee_id: str
    vehicle_id: str
    allocation_date: str

class AllocationHistory(BaseModel):
    employee_id: Optional[str] = None
    allocation_date: Optional[str] = None
