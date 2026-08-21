from datetime import datetime
from pydantic import BaseModel, Field

class SpotData(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    radius: int = Field(default=500, gt=0)

class SpotCreate(SpotData):
    pass

class SpotUpdate(SpotData):
    pass

class SpotRead(SpotData):
    id: int
    name: str
    longitude: float
    latitude: float
    radius: int
    created_at: datetime
    updated_at: datetime

