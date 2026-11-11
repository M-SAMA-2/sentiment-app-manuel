"""Raccord entre le modèle (src/predict.py) et le contrat de l'API."""
import sys
from pathlib import Path
from typing import TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele  # noqa: E402
from predict import predict as _predict  # noqa: E402

from api.schemas import Label  # noqa: E402

# Seuil d'abstention : sous 0,60, l'API répond INDETERMINE.
SEUIL_ABSTENTION = 0.60
CORRESPONDANCE: dict[str, Label] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (models/sentiment.joblib)"

    def __init__(self) -> None:
        modele = charger_modele()  # FileNotFoundError si le joblib manque
        inconnues = {str(c) for c in modele.classes_} - set(CORRESPONDANCE)
        if inconnues:
            raise ValueError(f"classes inconnues du contrat : {sorted(inconnues)}")

    def predict(self, text: str) -> Prediction:
        r = _predict(text)
        label: Label = "INDETERMINE" if r["score"] < SEUIL_ABSTENTION else CORRESPONDANCE[r["label"]]
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    return SentimentClassifier()