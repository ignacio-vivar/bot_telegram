from pydantic import BaseModel
from typing import List, Union

class FoodEntry(BaseModel):
    food_entry_name: str
    meal: str
    calories: float
    carbohydrate: float
    protein: float
    fat: float


class FoodEntriesResponse(BaseModel):
    food_entry: Union[List[FoodEntry], FoodEntry] 

class FatSecretRoot(BaseModel):
    food_entries: FoodEntriesResponse