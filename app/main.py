from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.errors import InvalidPokemonType, NoSearchResults, PokeApiTimeout, PokeApiUnavailable, PokemonNotFound
from app.services import get_pokemon, get_pokemon_by_type, search_pokemon

app = FastAPI()


@app.exception_handler(PokemonNotFound)
def pokemon_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": f"Pokemon '{exc}' not found"},
    )

@app.exception_handler(InvalidPokemonType)
def invalid_type_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": f"'{exc}' is not a valid Pokemon type"},
    )

@app.exception_handler(NoSearchResults)
def no_search_results_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": f"No Pokemon found matching '{exc}'"},
    )

@app.exception_handler(PokeApiTimeout)
def pokeapi_timeout_handler(request, exc):
    return JSONResponse(
        status_code=504,
        content={"error": "PokeAPI took too long to respond"},
    )


@app.exception_handler(PokeApiUnavailable)
def pokeapi_unavailable_handler(request, exc):
    return JSONResponse(
        status_code=502,
        content={"error": "PokeAPI is unavailable or returned an unexpected error"},
    )

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/pokemon/search")
def pokemon_search(name: str):
    return search_pokemon(name)


@app.get("/pokemon/{name_or_id}")
def pokemon_details(name_or_id: str):
    return get_pokemon(name_or_id)


@app.get("/pokemon")
def pokemon_by_type(type: str):
    return get_pokemon_by_type(type)

