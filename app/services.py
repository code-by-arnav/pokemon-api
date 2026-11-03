import httpx
from app.errors import EmptySearchQuery ,InvalidPokemonType, NoSearchResults, PokeApiTimeout, PokeApiUnavailable, PokemonNotFound


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
REQUEST_TIMEOUT = 5


def fetch(url):
    try:
        response = httpx.get(url, timeout=REQUEST_TIMEOUT)
    except httpx.TimeoutException:
        raise PokeApiTimeout()
    except httpx.RequestError:
        raise PokeApiUnavailable()
    if response.status_code >= 500:
        raise PokeApiUnavailable()
    return response


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
    response = fetch(url)
    if response.status_code == 404:
        raise PokemonNotFound(name_or_id)
    return clean_pokemon(response.json())

def search_pokemon(query):
    if not query.strip():
        raise EmptySearchQuery()
    url = f"{POKEAPI_BASE_URL}/pokemon?limit=100000"
    response = fetch(url)
    results = response.json()["results"]
    query = query.lower()
    matches = [p["name"] for p in results if query in p["name"]]
    if not matches:
        raise NoSearchResults(query)
    return {"count": len(matches), "results": matches}

def get_pokemon_by_type(type_name):
    url = f"{POKEAPI_BASE_URL}/type/{type_name.lower()}"
    response = fetch(url)
    if response.status_code == 404:
        raise InvalidPokemonType(type_name)
    entries = response.json()["pokemon"]
    names = [e["pokemon"]["name"] for e in entries]
    return {"count": len(names), "results": names}