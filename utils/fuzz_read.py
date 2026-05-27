import json
from pydantic import TypeAdapter
from thefuzz import process
from schemas.food_identifier import LocalFoodItem

with open("lib/alimentos.json", "r", encoding="utf-8") as f:
    data_as_list = json.load(f)
    CATALOGO_LOCAL: list[LocalFoodItem] = TypeAdapter(list[LocalFoodItem]).validate_python(data_as_list)

def buscar_alimento_en_catalogo(texto_ingresado: str) -> LocalFoodItem | None:
    """
    Aplana todos los alias de la base de datos, busca la mejor coincidencia
    y retorna el objeto con los IDs de FatSecret.
    """
    mapa_alias = {}
    for item in CATALOGO_LOCAL:
        for alias in item.aliases:
            mapa_alias[alias] = item
            
    lista_de_alias = list(mapa_alias.keys())
    
    mejor_match, porcentaje = process.extractOne(texto_ingresado, lista_de_alias)
    
    if porcentaje >= 75:
        return mapa_alias[mejor_match]
        
    return None
