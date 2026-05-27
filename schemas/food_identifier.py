from pydantic import BaseModel
from typing import List

class LocalFoodItem(BaseModel):
    nombre_limpio: str
    aliases: List[str]
    food_id: str
    serving_id: str
    unit_type: str
