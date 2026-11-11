# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Détecter automatiquement les ordonnances auxquelles il manque un élément obligatoire (identité du patient, médicament, posologie, durée, signature ou cachet du prescripteur) avant leur délivrance.

## Utilisateur final (obligatoire)

Le pharmacien ou le préparateur au comptoir, qui reçoit une alerte indiquant l'élément manquant et décide de contacter le prescripteur ou de refuser la délivrance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La liste des mentions obligatoires d'une ordonnance est connue, stable et fixée par la réglementation : une règle lisible permet d'expliquer précisément pourquoi une ordonnance est signalée. (d) Valider à tort une ordonnance incomplète peut conduire à une erreur de délivrance dangereuse pour le patient, donc le système doit être totalement prévisible et vérifiable, ce qu'un modèle statistique ne garantit pas.

## Données nécessaires et leur origine (obligatoire)

Un jeu d'ordonnances fictives ou anonymisées, complètes et volontairement incomplètes, créé par l'équipe à partir de la liste réglementaire des mentions obligatoires. Aucune ordonnance réelle n'est utilisée.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur un jeu de test de 50 ordonnances fictives, 100 % des ordonnances incomplètes doivent être signalées (rappel de 1,0), avec au plus 10 % de fausses alertes sur les ordonnances complètes.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une fausse alerte coûte quelques minutes au pharmacien, qui la contredit en un clic. Une omission est plus grave : le pharmacien garde donc la validation finale avant toute délivrance, le système ne bloque et ne valide rien seul.

## Risques éthiques ou de confidentialité (obligatoire)

Une ordonnance contient des données de santé, particulièrement sensibles (RGPD, loi 09-08) : anonymisation avant tout traitement, traitement en local sans envoi à un service tiers, et aucune conservation des ordonnances analysées.

## Approche écartée et pourquoi (facultatif)

Machine learning : écarté car il faudrait beaucoup d'ordonnances étiquetées, impossibles à obtenir pour des données de santé, et il ne garantirait pas de détecter chaque champ manquant.