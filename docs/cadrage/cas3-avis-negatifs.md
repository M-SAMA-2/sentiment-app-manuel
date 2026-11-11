## Besoin en une phrase (obligatoire)

Repérer automatiquement les avis négatifs d'un site e-commerce pour que le service client les traite en priorité.

## Utilisateur final (obligatoire)

L'équipe du service client, qui reçoit chaque matin une file d'avis triée, les plus négatifs en premier, au lieu de lire tous les avis.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(a) Le site dispose de milliers d'avis avec une note en étoiles, qui peut servir d'étiquette de départ à faible coût, et la tâche est répétitive. (c) Avec des milliers d'avis par jour, un classifieur coûte presque rien par requête, alors qu'un modèle génératif serait facturé à chaque appel. (d) Un avis mal classé retarde une réponse au client, sans conséquence grave, et un humain peut le corriger.

## Données nécessaires et leur origine (obligatoire)

Avis clients du site avec leur note, exportés puis anonymisés (noms, adresses, numéros de commande supprimés). Pour le TP, un jeu public ou fictif d'avis en français.

## Métrique de succès et seuil d'acceptation (obligatoire)

F1 macro d'au moins 0,85 sur un jeu de test tenu à l'écart, avec un rappel d'au moins 0,90 sur la classe négative, puisque c'est elle qu'il faut prioriser.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Un avis négatif classé positif est lu plus tard que prévu ; un avis positif classé négatif fait perdre un peu de temps. Quand la confiance du modèle est faible, l'avis est renvoyé à un conseiller du service client qui tranche.

## Risques éthiques ou de confidentialité (obligatoire)

Un avis peut contenir un nom, une adresse ou un numéro de commande : anonymisation avant tout traitement, stockage en interne, et conformité au RGPD et à la loi 09-08.

## Approche écartée et pourquoi (facultatif)

Règles par mots-clés (« nul », « déçu ») : elles ratent les formulations imprévues et la négation, comme « pas déçu ».