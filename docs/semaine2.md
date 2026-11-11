# Semaine 2 : le modèle de sentiment

## Mesures

- Données : jeu de démonstration de 290 avis (145 positifs, 145 négatifs), dont 100 avis mitigés et 30 neutres, volontairement difficiles.
- Découpage : 232 avis d'entraînement, 58 de test (80 % / 20 %, stratifié, graine 42).
- Modèle : pipeline TF-IDF (unigrammes et bigrammes) + régression logistique, vocabulaire de 316 termes.
- F1 macro sur le jeu de test : **0,879** (seuil d'acceptation : 0,85).

| Classe | Précision | Rappel | F1 |
| --- | --- | --- | --- |
| negative | 0,844 | 0,931 | 0,885 |
| positive | 0,923 | 0,828 | 0,873 |

Matrice de confusion (lignes = vérité, colonnes = prédiction) :

|  | negative | positive |
| --- | --- | --- |
| negative | 27 | 2 |
| positive | 5 | 24 |

## Analyse des erreurs

**Quelles erreurs.** Le modèle commet 7 erreurs sur 58 avis : 2 avis négatifs classés positifs et 5 avis positifs classés négatifs. Les trois exemples affichés par `evaluate.py` sont tous des avis mitigés construits avec un retournement (« …, sauf que ensuite … »). Le rappel de la classe positive (0,828) est plus faible que celui de la classe négative (0,931).

**Pourquoi.** TF-IDF représente un avis comme un sac de mots : il pondère les termes mais ignore leur ordre. Il compte donc les mots positifs et négatifs sans voir le retournement, alors que l'étiquette suit la seconde moitié de l'avis, celle qui conclut. Un bon score global (0,879) n'exclut pas des erreurs franches : l'avis « Colis abîmé, je suis déçu » est classé `positive` avec une confiance de 67 %, probablement parce que « abîmé » et « déçu » ne figurent pas dans le vocabulaire de 316 termes. Le score de confiance n'est donc pas une garantie de justesse.

**Comment les corriger.** Il faudrait une représentation qui tient compte du contexte et de l'ordre des mots, par exemple des embeddings de phrases (prévus en semaine 9), et un jeu de données plus grand et plus varié (le jeu Allociné). Un seuil d'abstention sur le score de confiance, avec renvoi vers un humain, ne rattraperait qu'une partie des erreurs, car certaines sont commises avec une confiance élevée.

## Limites

Ces mesures portent sur 58 avis générés : elles illustrent le processus, mais ne prouvent pas la performance sur des avis réels d'un autre domaine.