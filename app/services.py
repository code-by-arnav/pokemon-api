import httpx
from app.errors import PokemonNotFound
from app.errors import InvalidPokemonType, PokemonNotFound

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


def clean_pokemon(raw):
    sprites = raw.get("sprites") or {}
    other = sprites.get("other") or {}
    artwork = other.get("official-artwork") or {}
    return {
        "id": raw["id"],
        "name": raw["name"],
        "height": raw["height"],
        "weight": raw["weight"],
        "types": [t["type"]["name"] for t in raw["types"]],
        "abilities": [a["ability"]["name"] for a in raw["abilities"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in raw["stats"]},
        "sprite_url": artwork.get("front_default"),
    }

def get_pokemon(name_or_id):
    url = f"{POKEAPI_BASE_URL}/pokemon/{name_or_id}"
    response = httpx.get(url)
    if response.status_code == 404:
        raise PokemonNotFound(name_or_id)
    return clean_pokemon(response.json())

def search_pokemon(query):
    url = f"{POKEAPI_BASE_URL}/pokemon?limit=100000"
    response = httpx.get(url)
    results = response.json()["results"]
    query = query.lower()
    matches = [p["name"] for p in results if query in p["name"]]
    return {"count": len(matches), "results": matches}

def get_pokemon_by_type(type_name):
    url = f"{POKEAPI_BASE_URL}/type/{type_name.lower()}"
    response = httpx.get(url)
    if response.status_code == 404:
        raise InvalidPokemonType(type_name)
    entries = response.json()["pokemon"]
    names = [e["pokemon"]["name"] for e in entries]
    return {"count": len(names), "results": names}