import os
import asyncio
from requests_oauthlib import OAuth1Session
from schemas.food_response import FatSecretRoot, FoodEntry
from utils.get_today import get_today

# Las variables de entorno ya deberían estar cargadas desde main.py
CLIENT_ID = os.getenv('CONSUMER_KEY')
CLIENT_SECRET = os.getenv('CONSUMER_SECRET')
USER_TOKEN = os.getenv('ACCESS_KEY')
USER_SECRET = os.getenv('ACCESS_SECRET')

# Instancia global de la sesión
fatsecret_user = OAuth1Session(
    CLIENT_ID,
    client_secret=CLIENT_SECRET,
    resource_owner_key=USER_TOKEN,
    resource_owner_secret=USER_SECRET
)

async def get_today_food() -> list[FoodEntry]:
    api_url = "https://platform.fatsecret.com/rest/food-entries/v2"
    delta_days = get_today()

    params = {
    "format": "json",
    "date": delta_days # FatSecret v1 espera este entero
    }

    # Ejecutamos la petición síncrona en un hilo separado
    response = fatsecret_user.get(api_url, params=params)

    if response.status_code == 200:
        raw_data = response.json()
        
        # Pydantic valida y limpia el JSON automáticamente acá
        validated_data = FatSecretRoot(**raw_data)
        
        entradas = validated_data.food_entries.food_entry
        
        # Normalizamos para devolver siempre una lista, incluso si hay 1 sola comida
        if isinstance(entradas, list):
            return entradas
        else:
            return [entradas]
    else:
        # Aquí podrías manejar el error de forma más elegante
        print(f"Error {response.status_code}: {response.text}")
        return []