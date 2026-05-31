import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
from utils.get_today import get_today
from utils.fuzz_read import buscar_alimento_en_catalogo

# Cargamos el archivo .env a la memoria
load_dotenv()

CLIENT_ID = os.getenv('CONSUMER_KEY')
CLIENT_SECRET = os.getenv('CONSUMER_SECRET')
USER_TOKEN = os.getenv('ACCESS_KEY')
USER_SECRET = os.getenv('ACCESS_SECRET')

fatsecret_user = OAuth1Session(CLIENT_ID,
                               client_secret=CLIENT_SECRET,
                               resource_owner_key=USER_TOKEN,
                               resource_owner_secret=USER_SECRET)


async def post_food(meal_sel: str, quantity: str, input_food: str ) -> None:
    api_url = "https://platform.fatsecret.com/rest/food-entries/v1"

    


    delta_days = get_today()

    food_data = buscar_alimento_en_catalogo(input_food)
    if not food_data:
        return "not_found", ""

    quantity = str(float(quantity))
   

    params = {
        "food_id": food_data.food_id,
        "food_entry_name": food_data.nombre_limpio,
        "serving_id": food_data.serving_id,
        "number_of_units": quantity,
        "meal": meal_sel,
        "date": delta_days,
        "format": "json"
    }

    try:
        response = fatsecret_user.post(api_url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return "not_post", ""
            unidad = getattr(food_data, "unit_type", "")
            return "ok", unidad
        else:
            return "not_post", ""
    except Exception:
        return "failed", ""