"""Tests de l'API, sans serveur : TestClient branche le client sur l'application."""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le "with" déclenche lifespan (chargement du modèle)
        yield c


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["docs"] == "/docs"


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "OK"
    assert "sentiment.joblib" in body["model"]


def test_predict_contrat(client):
    r = client.post("/predict", json={"text": "Livraison rapide, produit conforme, très satisfait"})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0.5 <= body["score"] <= 1.0
    assert body["text"].startswith("Livraison rapide")


def test_abstention_sous_le_seuil(client, monkeypatch):
    """Sous le seuil, l'API répond INDETERMINE quelle que soit la classe prédite."""
    import api.model as m

    monkeypatch.setattr(m, "_predict", lambda texte: {"label": "positive", "score": 0.55})
    r = client.post("/predict", json={"text": "avis quelconque"})
    assert r.status_code == 200
    assert r.json()["label"] == "INDETERMINE"
    assert r.json()["score"] == 0.55


def test_pas_d_abstention_au_dessus_du_seuil(client, monkeypatch):
    import api.model as m

    monkeypatch.setattr(m, "_predict", lambda texte: {"label": "negative", "score": 0.90})
    r = client.post("/predict", json={"text": "avis quelconque"})
    assert r.json()["label"] == "NEGATIVE"


@pytest.mark.parametrize("corps", [{"text": ""}, {"text": "   "}, {}, {"text": "a" * 2001}])
def test_predict_refus_422(client, corps):
    assert client.post("/predict", json=corps).status_code == 422