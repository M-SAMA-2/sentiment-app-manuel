# Compte rendu global des TP1 à TP3

**Auteur :** [FENNANE MEHDI] ([@M-SAMA-2])
**Dépôt :** https://github.com/M-SAMA-2/sentiment-app-manuel
**Date :** 11/11/2026

J'ai réalisé ce projet seul, sans binôme. Une conséquence visible : le test `test_each_member_has_committed` échoue (1 auteur de commits au lieu de 2), donc `pytest -q` affiche `44 passed, 1 failed` et non `45 passed`.

## 1. Le besoin et son cadrage

Un site e-commerce reçoit des milliers d'avis clients en français et veut traiter en priorité les avis négatifs. L'équipe relation client ne peut pas tout lire : il faut un tri automatique qui signale les avis négatifs et qui renvoie à un humain ceux dont le sentiment est incertain.

L'approche retenue pour le cas 3 est le **machine learning** [à vérifier avec votre fiche cas3-avis-negatifs.md : reprenez la case que vous avez cochée]. Ma justification s'appuie sur les critères (a), (c) et (d). Critère (a), données étiquetées : un avis est accompagné d'une note ou peut être étiqueté à faible coût, et la tâche est répétitive. Critère (c), coût par requête : avec des milliers d'avis par jour, un classifieur coûte presque rien par avis, alors qu'un modèle génératif facturerait chaque appel. Critère (d), conséquence d'une erreur : un avis mal classé se corrige par une relecture humaine, la conséquence est faible. Les règles métier sont écartées car la façon d'exprimer une insatisfaction n'a pas de logique stable (« pas déçu » n'est pas « déçu »), et le RAG ne s'applique pas car la réponse ne vient pas d'un document à citer.

## 2. L'architecture du dépôt

- `src/` : le code du modèle (`make_demo.py`, `train.py`, `evaluate.py`, `predict.py`).
- `ui/` : l'interface Streamlit (`app.py` pour l'affichage, `helpers.py` pour la logique).
- `tests/` : les tests (environnement, fiches de cadrage, historique Git, modèle, interface).
- `docs/` : les fiches de cadrage, les comptes rendus hebdomadaires et ce document.
- `data/` et `models/` : les données et le modèle produits localement.
- `scripts/` : le diagnostic (`check_setup.py`) et les utilitaires de mise en place.
- `.github/workflows/` : l'intégration continue.

Ce qui n'est **pas** versionné : `.venv/`, `.env`, `models/sentiment.joblib` et `data/demo_reviews.csv`. L'environnement et les secrets n'ont rien à faire dans le dépôt, et les deux autres fichiers se reconstruisent à l'identique par `python src/make_demo.py` et `python src/train.py`, grâce à la graine aléatoire fixée à 42.

**Pourquoi `models/metrics.json` est dans Git et pas `models/sentiment.joblib` ?** Le modèle est un binaire volumineux, reconstructible, qui alourdirait chaque version de l'historique. Les métriques sont un petit fichier lisible qui décrit la qualité du modèle. Elles sont indispensables à la CI : elle n'a jamais le modèle, mais elle lit `metrics.json` pour vérifier que le F1 dépasse le seuil d'acceptation de 0,85.

## 3. Le modèle

**Données.** Deux jeux : un jeu de démonstration de 290 avis générés (145 positifs, 145 négatifs, dont 100 mitigés et 30 neutres, volontairement