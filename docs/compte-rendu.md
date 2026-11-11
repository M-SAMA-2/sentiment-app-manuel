# Compte rendu global des TP1 à TP3

**Auteur :** FENNANE MEHDI (GitHub : @M-SAMA-2)
**Dépôt :** https://github.com/M-SAMA-2/sentiment-app-manuel
**Date :** 11/11/2026

J'ai réalisé ce projet seul, sans binôme. Une conséquence visible : le test `test_each_member_has_committed` échoue (1 auteur de commits au lieu de 2), donc `pytest -q` affiche `44 passed, 1 failed` et non `45 passed`.

## 1. Le besoin et son cadrage

Un site e-commerce reçoit des milliers d'avis clients en français et veut traiter en priorité les avis négatifs. L'équipe du service client ne peut pas tout lire : il faut un tri automatique qui signale les avis négatifs et qui renvoie à un humain ceux dont le sentiment est incertain.

L'approche retenue pour le cas 3 est le **machine learning**. Ma justification s'appuie sur les critères (a), (c) et (d). Critère (a), données étiquetées : le site dispose de milliers d'avis avec une note en étoiles, qui peut servir d'étiquette de départ à faible coût, et la tâche est répétitive. Critère (c), coût par requête : avec des milliers d'avis par jour, un classifieur coûte presque rien par avis, alors qu'un modèle génératif serait facturé à chaque appel. Critère (d), conséquence d'une erreur : un avis mal classé retarde une réponse au client, sans conséquence grave, et un humain peut le corriger. Les règles par mots-clés sont écartées car elles ratent les formulations imprévues et la négation (« pas déçu » n'est pas « déçu »), et le RAG ne s'applique pas car la réponse ne vient pas d'un document à citer.

## 2. L'architecture du dépôt

- `src/` : le code du modèle (`make_demo.py`, `train.py`, `evaluate.py`, `predict.py`).
- `ui/` : l'interface Streamlit (`app.py` pour l'affichage, `helpers.py` pour la logique, testable sans lancer Streamlit).
- `tests/` : les tests (environnement, fiches de cadrage, historique Git, modèle, interface).
- `docs/` : les fiches de cadrage, les comptes rendus hebdomadaires et ce document.
- `data/` et `models/` : les données et le modèle produits localement.
- `scripts/` : le diagnostic (`check_setup.py`) et les utilitaires de mise en place.
- `.github/workflows/` : l'intégration continue.

Ce qui n'est **pas** versionné : `.venv/`, `.env`, `models/sentiment.joblib` et `data/demo_reviews.csv`. L'environnement et les secrets n'ont rien à faire dans le dépôt, et les deux autres fichiers se reconstruisent à l'identique par `python src/make_demo.py` et `python src/train.py`, grâce à la graine aléatoire fixée à 42.

**Pourquoi `models/metrics.json` est-il dans Git et pas `models/sentiment.joblib` ?** Le modèle est un binaire volumineux et reconstructible, qui alourdirait chaque version de l'historique. Les métriques sont un petit fichier lisible qui décrit la qualité du modèle. Elles sont indispensables à la CI : elle n'a jamais le modèle, mais elle lit `metrics.json` pour vérifier que le F1 dépasse le seuil d'acceptation de 0,85.

## 3. Le modèle

**Données.** Deux jeux : un jeu de démonstration de 290 avis générés (145 positifs, 145 négatifs, dont 100 mitigés et 30 neutres, volontairement difficiles), et le jeu Allociné de 20 000 critiques de films en français (10 204 négatives).

**Découpage et pipeline.** Chaque jeu est coupé en 80 % d'entraînement et 20 % de test, de façon stratifiée (`random_state=42`). Le découpage est fait **avant** toute vectorisation : sinon le vocabulaire TF-IDF aurait « vu » les avis de test et le score serait trop optimiste (fuite de données). Le `Pipeline` enchaîne un `TfidfVectorizer` (mots et paires de mots, `min_df=2`, `sublinear_tf=True`) et une `LogisticRegression` (`class_weight="balanced"`). Un seul objet est sauvegardé : la transformation appliquée au texte en production est forcément celle de l'entraînement.

| Jeu | Avis | Vocabulaire | F1 macro | Rappel négatif |
| --- | --- | --- | --- | --- |
| Démonstration | 290 (232 train / 58 test) | 316 | 0,879 | 0,931 |
| Allociné | 20 000 (16 000 train / 4 000 test) | 149 529 | 0,9205 | 0,9113 |

L'exactitude vaut 0,8793 sur la démonstration et 0,9205 sur Allociné. Les valeurs d'Allociné sont celles de mon `models/metrics.json` actuel ; celles de la démonstration viennent de l'exécution de `python src/train.py` et de l'historique Git.

**Matrice de confusion sur la démonstration** (lignes = vérité, colonnes = prédiction) :

```text
            negative  positive
  negative        27         2
  positive         5        24
```

Ligne « negative » : sur 29 avis négatifs, 27 sont retrouvés et 2 sont classés positifs, d'où un rappel négatif de 27/29 = 0,931. Ligne « positive » : sur 29 avis positifs, 24 sont retrouvés et 5 sont classés négatifs. Le modèle se trompe donc plus souvent sur les positifs (5 erreurs) que sur les négatifs (2 erreurs). Au total, 7 erreurs sur 58 avis.

Mes valeurs sont identiques à celles du kit de référence (0,879 et 0,920), ce qui confirme que les versions figées de scikit-learn (1.5.2) et pandas (2.2.3) reproduisent bien l'expérience.

## 4. L'analyse des erreurs

Sur la démonstration, les 7 erreurs sont toutes des avis mitigés, construits avec un retournement. Exemple tiré de mes données : « Commande jamais reçue et remboursement en attente au début, sauf que ensuite je recommande » est un avis positif prédit négatif. Autre exemple : « Service impeccable et livraison en avance sur le papier, sauf que ensuite produit cassé » est un avis négatif prédit positif.

**Mécanisme.** TF-IDF représente un avis comme un sac de mots : il compte les termes mais ignore leur ordre. Le modèle additionne des mots négatifs et des mots positifs, mais ne voit pas que le retournement (« sauf que ensuite ») donne la conclusion de l'avis, alors que l'étiquette suit la seconde moitié. Les bigrammes aident un peu (« pas déçu »), mais ils ne couvrent pas une inversion à l'échelle de la phrase.

**Un second phénomène : le changement de domaine.** Le modèle Allociné a appris sur des critiques de films. Sur l'avis « Colis abîmé, je suis déçu », le modèle de démonstration répond `positive` avec 67 % de confiance (faux), et le modèle Allociné répond `negative` avec 88 % (juste). En revanche, l'avis nettement positif « Livraison rapide, produit conforme, très satisfait » obtient 50 % et « penche vers négatif » avec le modèle Allociné, car des mots comme « livraison » et « conforme » sont rares dans des critiques de films. Appliqué à l'ensemble de `demo_reviews.csv`, le modèle Allociné fait 22 erreurs sur 290 (7,6 %), contre 7 sur 58 (12 %) pour le modèle de démonstration sur son propre jeu de test ; ces deux chiffres ne portent pas sur les mêmes avis et ne se comparent pas directement. Un F1 de 0,92 mesuré sur des films ne garantit rien pour des avis de produits. Une confiance élevée n'est pas non plus une garantie de justesse : le modèle de démonstration affichait 67 % en se trompant.

**Pour corriger.** Il faudrait des représentations qui tiennent compte de l'ordre et du contexte (embeddings de phrases, abordés plus tard dans le cours) et surtout des avis étiquetés du domaine réel (livraison, produit). Ce n'était pas le sujet de ces séances, qui portaient sur la chaîne complète plutôt que sur la performance maximale.

## 5. L'interface et le seuil d'incertitude

L'interface Streamlit appelle directement la fonction `predict()` du TP2 et affiche « à vérifier » quand la confiance est strictement inférieure au seuil `SEUIL_INCERTITUDE`. Je retiens **0,60**. Les effectifs viennent de l'export de l'interface sur `demo_reviews.csv` (290 avis, modèle Allociné) :

| Seuil | Avis envoyés à un agent |
| --- | --- |
| 0,50 | 0 |
| 0,60 | 69 (24 %) |
| 0,75 | 137 (47 %) |

À 0,50, le seuil ne filtre