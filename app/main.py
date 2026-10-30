from fastapi import FastAPI

from app.services import get_pokemon, search_pokemon

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/pokemon/search")
def pokemon_search(name: str):
    return search_pokemon(name)


@app.get("/pokemon/{name_or_id}")
def pokemon_details(name_or_id: str):
    return get_pokemon(name_or_id)