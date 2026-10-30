from fastapi import FastAPI

from app.services import get_pokemon

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/pokemon/{name_or_id}")
def pokemon_details(name_or_id: str):
    return get_pokemon(name_or_id)