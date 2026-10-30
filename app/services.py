import httpx

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


def clean_pokemon(raw):
    return {
        "id": raw["id"],
        "name": raw["name"],
        "height": raw["height"],
        "weight": raw["weight"],
        "types": [t["type"]["name"] for t in raw["types"]],
    }


def get_pokemon(name_or_id):
    url = f"{POKEAPI_BASE_URL}/pokemon/{name_or_id}"
    response = httpx.get(url)
    return clean_pokemon(response.json())