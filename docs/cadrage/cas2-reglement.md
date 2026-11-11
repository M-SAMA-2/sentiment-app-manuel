## Besoin en une phrase (obligatoire)

Répondre aux questions des élèves et des parents sur le règlement intérieur de l'école, en citant l'article concerné.

## Utilisateur final (obligatoire)

Les élèves et leurs parents, qui obtiennent une réponse immédiate avec l'article cité ; l'administration (CPE) reste l'interlocuteur en cas de doute.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La réponse doit pouvoir être tracée jusqu'à l'article du règlement : le RAG retrouve les passages du document et les cite, ce qu'un modèle génératif seul ne garantit pas. (a) Il n'existe pas de jeu de questions étiquetées avec leur bonne réponse, alors que le règlement existe déjà sous forme de document, ce qui écarte le machine learning. (d) Une réponse fausse peut conduire à une sanction injustifiée, d'où l'importance de la source citée.

## Données nécessaires et leur origine (obligatoire)

Le texte officiel du règlement intérieur, découpé par articles, fourni par l'administration. Pour les tests, une trentaine de questions fictives écrites à la main, sans aucune donnée personnelle d'élève.

## Métrique de succès et seuil d'acceptation (obligatoire)

Sur 30 questions de test rédigées à la main, au moins 90 % des réponses citent le bon article, et 100 % des questions hors règlement reçoivent la réponse « je ne sais pas, voir l'administration ».

## Conséquence d'une erreur et validation humaine prévue (obligatoire)

Une réponse erronée peut induire un élève ou un parent en erreur. Chaque réponse affiche l'article cité, et toute décision disciplinaire reste prise par la CPE ou la direction, jamais par le système.

## Risques éthiques ou de confidentialité (obligatoire)

Les questions peuvent révéler la situation d'un élève : aucune question n'est conservée avec un nom, les journaux sont anonymisés, et le système n'envoie rien à un service tiers sans accord de l'école.

## Approche écartée et pourquoi (facultatif)

Machine learning : aucune question étiquetée n'existe, et un classifieur ne citerait pas l'article source.