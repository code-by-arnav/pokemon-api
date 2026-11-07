from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

FAKE_PIKACHU = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": [{"slot": 1, "type": {"name": "electric"}}],
    "abilities": [{"ability": {"name": "static"}}],
    "stats": [{"base_stat": 35, "stat": {"name": "hp"}}],
    "sprites": {"other": {"official-artwork": {"front_default": "https://example.com/25.png"}}},
}


class FakeResponse:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data


def test_pokemon_details_success(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(200, FAKE_PIKACHU)

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon/pikachu")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "pikachu"
    assert body["types"] == ["electric"]
    assert body["abilities"] == ["static"]
    assert body["stats"] == {"hp": 35}
    assert body["sprite_url"] == "https://example.com/25.png"


def test_pokemon_not_found(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(404, {"status": 404, "message": "Not Found"})

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon/notapokemon")

    assert response.status_code == 404
    assert "notapokemon" in response.json()["error"]

FAKE_TYPE_ELECTRIC = {
    "pokemon": [
        {"slot": 1, "pokemon": {"name": "pikachu"}},
        {"slot": 1, "pokemon": {"name": "raichu"}},
    ]
}

FAKE_POKEMON_LIST = {
    "results": [
        {"name": "pikachu"},
        {"name": "pikachu-belle"},
        {"name": "bulbasaur"},
    ]
}

def test_filter_by_type_success(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(200, FAKE_TYPE_ELECTRIC)

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon?type=electric")

    assert response.status_code == 200
    assert response.json() == {"count": 2, "results": ["pikachu", "raichu"]}


def test_invalid_type(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(404, {"status": 404, "message": "Not Found"})

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon?type=banana")

    assert response.status_code == 400


def test_search_success(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(200, FAKE_POKEMON_LIST)

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon/search?name=pika")

    assert response.status_code == 200
    assert response.json() == {"count": 2, "results": ["pikachu", "pikachu-belle"]}


def test_search_no_matches(monkeypatch):
    def fake_fetch(url):
        return FakeResponse(200, FAKE_POKEMON_LIST)

    monkeypatch.setattr("app.services.fetch", fake_fetch)

    response = client.get("/pokemon/search?name=zzzzz")

    assert response.status_code == 404