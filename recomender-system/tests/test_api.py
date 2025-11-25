"""
Testes automatizados da API de Sistema de Recomendação

"""

from fastapi.testclient import TestClient
import sys, os

# Ajuste de path para importar a API

BASE_DIR = os.path.dirname(__file__)
APP_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "app"))
sys.path.append(APP_DIR)

from main import app

client = TestClient(app)


# Testes Básicos

def test_homepage():
    """Testa se a homepage carrega corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()


def test_best_seller_ratings():
    """Verifica se o ranking por nota retorna JSON válido."""
    response = client.get("/best-seller/ratings/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    if len(data) > 0:
        assert "movieId" in data[0]


def test_most_viewed():
    """Verifica ranking por quantidade de avaliações."""
    response = client.get("/best-seller/views/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)


def test_search_movie():
    """Testa busca simples por nome de filme."""
    response = client.get("/search/movie/toy")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Testes de Inserção de Dados


def test_add_user():
    """
    Testa inclusão de novo usuário.
    Obs.: Se o usuário já existe, o endpoint retorna 400.
    """
    response = client.post("/users/", json={"user_id": 999999})
    assert response.status_code in (200, 400)


def test_add_movie():
    """
    Testa inclusão de um novo filme.
    Como o ID pode já existir, aceitamos 200 ou 400.
    """
    payload = {
        "movieId": 999999,
        "title": "Test Movie",
        "genres": "Test"
    }

    response = client.post("/movies/", json=payload)
    assert response.status_code in (200, 400)


def test_update_rating():
    """
    Testa criação/atualização de rating para filme.
    """
    payload = {
        "user_id": 12345,
        "movie_id": 1,   # existe no dataset
        "rating": 4.5
    }

    response = client.post("/ratings/", json=payload)
    assert response.status_code == 200
    json_resp = response.json()
    assert "rating" in json_resp


# Testes de Recomendações

def test_similarity_recommendations():
    """Testa recomendação item-based para um filme existente."""
    response = client.get("/similarity/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_user_based_recommendation():
    """
    Testa recomendação user-based.
    Obs.: Alguns userId podem não existir no dataset.
    """
    response = client.get("/user-based/1")
    assert response.status_code in (200, 404)
