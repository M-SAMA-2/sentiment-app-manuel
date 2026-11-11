"""Le contrat de l'API, écrit dans des types."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class PredictRequest(BaseModel):
    """Requête de prédiction."""

    text: str = Field(
        ..., min_length=1, max_length=2000, description="Texte à classifier",
        examples=["Livraison rapide, produit conforme, très satisfait"],
    )

    @field_validator("text")
    @classmethod
    def refuser_texte_blanc(cls, valeur: str) -> str:
        """Un texte vide une fois ses blancs retirés est refusé."""
        if not valeur.strip():
            raise ValueError("texte vide une fois les blancs retirés")
        return valeur


class PredictResponse(BaseModel):
    label: Label
    score: float
    text: str


class HealthResponse(BaseModel):
    status: str
    model: str