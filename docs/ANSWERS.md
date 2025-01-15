# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

## **Environnement de Test**

- **Version de Python** : 3.10.8
- **OS testé**: MacOs 14.6.1 (Devrait aussi fonctionner sur les versions modernes de GNU/Linux).

## **Contexte**

Cette partie vise à expliquer les choix techniques effectués dans la réalisation de la solution.

1. **Environnement virtuel**
    -   J’ai choisi venv pour privilégier la simplicité.
    -   J’aurais pu me tourner vers d’autres méthodes de virtualisation, comme Docker ou des solutions préconfigurées (ex. conda), mais cela aurait ajouté de la complexité et de nouvelles dépendances sans offrir une valeur ajoutée significative à la solution.
    -   Cependant, si l’on devait charger les données en base de données après extraction et transformation, Docker serait utile pour automatiser le déploiement de l’infrastructure (création d’un conteneur pour la BDD, etc.). En effet, ça réduirait considérablement le temps pour reproduire et configurer l’environnement complet.

2. **Choix de Python et requests**
    - La solution repose uniquement sur Python et la librairie requests pour le flux de données.
    - Cela marche parce que le volume de données traité est actuellement assez faible, privilégiant la facilité de développement plutôt que des solutions plus lourdes (Spark, etc.).
    - Toutefois, dans une application de type Spotify où le flux pourrait devenir énorme, on aurait pu envisager des solutions distribuées ou parallélisables comme Dask ou Spark (PySpark) pour gérer la scalabilité.

3. **Tests unitaires**
    - J’ai inclus des tests unitaires, même s’ils ne sont pas exhaustifs, notamment sur `transform.py` et `load.py`.
    - On peut facilement imaginer des améliorations futures (plus de tests, couverture plus large).
    - De plus, on pourrait mettre en place un pipeline de CI (via GitHub Actions) déclenché à chaque push, afin de lancer tous les tests automatiquement.

4. **Validation du schéma vs. intégrité des données**
    - J’ai privilégié la validation du schéma : les lignes qui ne valident pas le schéma sont écartées.
    -  Dans la vraie vie, on s’adapterait selon la future utilisation de ces données (discussion avec les stakeholders). Par exemple, les champs email, gender, favorite_genres ne sont peut-être pas indispensables pour la recommandation.
    - On pourrait aussi archiver les lignes non conformes, plutôt que les ignorer. Je n’ai pas mis en place ce mécanisme ici, sachant que les données respectent déjà le schéma.

5. **Flux de données quotidien**
    - Le fait qu’il soit quotidien ne précise pas si cela renvoie uniquement les nouveaux utilisateurs/tracks ou si cela inclut toutes les données à chaque fois.
    - On pourrait adapter la solution selon ce comportement dans des améliorations futures.
    - Par ailleurs, un point non traité : il se peut que certains listen_history contiennent des user_id ou track_id invalides ou qui n’existent pas encore localement, causant potentiellement des problèmes en aval.
    - Il faudrait vérifier l’intégrité de ces IDs en les comparant à ceux que l’on possède déjà (via une hashmap par exemple).

6. **Consistance des noms de colonnes**
    - J’ai conservé la cohérence avec les noms de l’API (ex. songwriters, favorite_genres), même s’ils sont au pluriel pour un seul élément.
    - On pourrait normaliser : soit créer une table séparée pour la relation “un-à-plusieurs”, soit renommer ces champs au singulier si cela reflète mieux la réalité.
    - Pour éviter la confusion, j’ai gardé la cohérence entre avant et après le flux.
    - J'ai transformé le champs duration en secondes pour faciliter l'utilisation des données en aval.
    - Le champs "items" a été aussi applati dans les historique d'écoutes pour faciliter l'utilisation en aval des données après chargement.

7. **Utilisation de pandas**
    - J’utilise pandas pour simplifier l’écriture vers les fichiers CSV.
    - Si le volume de données augmente, on pourrait se tourner vers Dask ou Spark pour éviter les problèmes de performance.

8. **Automatisation (Crontab, GitHub Workflow, Airflow)**
    - Crontab est utilisé pour lancer le pipeline quotidiennement sur une machine locale.
    - Une autre approche : un GitHub Workflow avec un cron, qui chargerait la dernière version d’un CSV depuis un bucket, écrirait les nouvelles lignes, puis enregistrerait le tout en tant que nouveau fichier.
    - Enfin, des solutions comme Airflow pourraient être pertinentes si le projet prend de l’ampleur (gestion avancée des dépendances, monitoring, etc.).



## **Éxécution sur machine locale**

### **Création de  l'environment virtuelle**

- `python3 -m venv venv`

### **Activation de l'environnmenent**

- `source venv/bin/activate`  # Sur macOS/Linux \
- `.\venv\Scripts\activate`   # Sur Windows

### **Installation des dépendance nécessaires**

- `pip3 install -r requirements.txt`

### **Désactivation de l'environnement**

- `deactivate`

### **Activation de l'API moovitamix**

Pour activer l'API on peut suivre les instructions fournies dans le README suivant, [Instructions](../README.md).

### **Éxécution du flux de données en local**

Placer vous à la racine du dossier après avoir activé l'environnement virtuel et l'API et lancer la commande
- `python3 src/etl/pipeline.py`

### **Exécution des tests unitaires**

Pour rouler les tests unitaires, il faut se placer à la racine du projet après avoir et lancer la commande
- `pytest`

Si on a une erreur **ModuleNotFoundError: No module named 'src'**
- `PYTHONPATH=$(pwd) pytest`

### **Automatisation de la collecte des données**

- Prérequis: avoir installer l'environnement d'éxecution
Utiliser la commande suivant à partir de la racine du projet pour avoir le chemin de fichier absolu jusqu'au projet et le copier.
- `pwd`

Modifier votre crontab en utilisant la commande:
- `crontab - e`

Y ajouter la ligne suivante en mettant votre chemin absolu à la place des accolades:
- `0 1 * * * {chemin_absolu}/run_pipeline.sh >> {chemin_absolu}/technical-test-data-engineer/run_pipeline.log 2>&1`

Sur macOS vous risquez de devoir de donner à cron l'accès complet à votre disque pour que ce dernier puisse lancer le script.
À partir de là la collecte de données s'effectue tout les jours à 1h du matin.

## Questions (étapes 4 à 7)

### Étape 4

- Si les recommandations sont générées de façon asynchrone (par exemple, une fois par jour), stocker les données au format CSV dans une solution type data lake (AWS S3 ou Google Cloud Storage) me semble judicieux. On y gagne un accès facile aux données tout en réduisant considérablement les coûts d’infrastructure.

- En revanche, si les données doivent être exploitées en production (par exemple, pour d’autres fonctionnalités en temps réel), alors une base de données relationnelle (SQL) s’avère plus adaptée. En effet, nous avons des données hautement relationnelles et un schéma simple peu susceptible d’évoluer. Choisir une autre méthode risquerait de dégrader les performances sur les requêtes d’agrégation ou de jointure.
Dans ce cas là, PostgreSQL serait un excellent choix. Et si la charge de données augmente, il deviendra pertinent de réfléchir à une base de données managées sur le cloud comme rds ou redshift\bigquery (si on veut juste stocker sans utilisation en production).

Dans tout les cas, on peut s'imaginer stocker les données avec les tables suivantes:

**Table users**
| Column              | Datatype       |
|---------------------|----------------|
| id (clé primaire)   | INTEGER        |
| first_name          | TEXT           |
| last_name           | TEXT           |
| email               | TEXT           |
| gender              | TEXT           |
| favorite_genres     | TEXT           |
| created_at          | DATETIME       |
| updated_at          | DATETIME       |


**Table tracks**
| Column              | Datatype       |
|---------------------|----------------|
| id (clé primaire)   | INTEGER        |
| name                | TEXT           |
| artist              | TEXT           |
| songwriters         | TEXT           |
| duration            | INTEGER        |
| genres              | TEXT           |
| album               | TEXT           |
| created_at          | DATETIME       |
| updated_at          | DATETIME       |


**Table listen_history:**
| Column                   | Datatype       |
|--------------------------|----------------|
| listen_id (clé primaire) | INTEGER        |
| user_id (clé étrangère)  | INTEGER        |
| track_id (clé étrangère) | INTEGER        |
| created_at               | DATETIME       |
| updated_at               | DATETIME       |

On peut réfléchir à indexer la base de données sur les clés primaires des tables pour améliorer les performances lorsque des requêtes de join sont faites.

### Étape 5

#### **Méthode de surveillance**

1. **Logging**
    - Dans la solution, on se sert de nombreux logs pour tracer chaque étape du pipeline du flux de données (extraction, transformation, chargement).
    - C’est efficace pour repérer rapidement quand et où survient un problème.

2. **Suivi du volume de données**
    - Après chaque extraction ou chaque écriture de CSV, on log le nombre d’items traités.
    - Cette mesure du volume de données est utile pour détecter des irrégularités :
        - Une baisse soudaine d’items pointe peut-être vers un souci du côté de l’API ou des filtres.
        - Une hausse inhabituelle pourrait révéler un bug entraînant des doublons ou un mauvais calcul de pagination.

3. **Gestion des validations et des échecs**

    - Les tests unitaires (même s’ils ne tournent pas en production) donnent un aperçu de la logique de validation : par exemple, on ignore les lignes dont les champs obligatoires manquent.
    - En production, on peut aller plus loin :
        - Compter les lignes rejetées (non-conformes au schéma).
        - Définir un seuil à partir duquel on envoie une alerte (par e-mail ou Slack).

4. **Notificatios et suivi du pipeline**

    - En l’état, le pipeline affiche simplement « ETL pipeline finished successfully » dans les logs tout en redirigeant la sortie standard et l’erreur standard dans un fichier log local.
    - Une amélioration possible serait d'envoyer un petit rapport quotidien (par e-mail ou via un bot Slack) contenant le temps total d’exécution, le nombre d’items extraits et chargés, et les éventuelles erreurs détectées (HTTP, JSON invalide, etc.).
    - On pourrait passer par un orchestrateur plus poussé tel que Airflow afin de voir le statut de chaque tâche, recevoir des alertes automatiques en cas d’échec, et disposer de tableaux de bord pour analyser la performance du pipeline. Si on souhaite avoir une surveillance encore plus fine des logs on peut aussi se tourner vers un service de logs tel cloudwatch ou datadog.

#### **Les Métriques clés**
0
- **Nombre d’items extraits**, par endpoint (tracks, users, listen_history), afin de surveiller ce qui est vraiment récupéré au quotidien.

- **Le Taux d’erreur / Avertissements** soit le nombre d’erreurs HTTP (4xx, 5xx) ou d’erreurs JSON, en proportion du nombre de requêtes totales .

- **Les temps d'exécution**, on puet distinguer les temps d’extraction, de transformation et de chargement, histoire de cibler d’éventuels goulots d’étranglement.

- **La taille des fichiers de sortie**, une explosion de la taille des fichiers csv peut signaler un souci (duplications de lignes) ou, au contraire, une diminution brutale peut montrer que l’API ne renvoie plus autant de données.

- **Taux de duplications ou de rejets**, si on duplique des données à l’écriture (avant méthode de chargement), compter combien de doublons sont filtrés lors du chargement en proportion du nombre de ligne totale. On peut faire la même chose pour toutes les données refusées pour non-conformité au schéma.

### Étape 6

Estimons qu'on se base sur un algorithme de collaborative filtering utilisant la méthode des moindres carrés alternés (ALS, Alternating Least Squares) pour générer des recommandations destinées aux utilisateurs.
Je pars également du principe que les fichiers de sortie du flux de données sont sauvegardés sous forme de fichiers CSV locaux ou dans une solution de data lake (S3, Google Cloud Storage).

1. **Traitement des données**
    - Le traitement des données nécessaires pour les recommandations peut commencer une fois que nous avons reçu le dernier lot du flux de données (via Airflow).
    - Nous construisons une matrice où les lignes représentent les utilisateurs et les colonnes les chansons. Les valeurs de cette matrice correspondent au feedback de l'utilisateur pour une chanson donnée. Ici, le nombre d'écoutes d'une chanson semble être une mesure pertinente pour quantifier ce feedback.
    - On peut choisir de prendre uniquement les écoute de chansons qui ont été récentes (les écoutes lors de la dernière année, lors du dernier mois) en fonction des besoin de recommendations.

    - Outils de traitement :

        - Si la taille de la matrice reste relativement petite, Python avec scikit-learn peut suffire.
        - Cependant, comme ce type d'algorithme fonctionne mieux avec un grand nombre d'utilisateurs, la taille de la matrice risque d'être conséquente. Dans ce cas, l'utilisation de Spark MLlib (framework de calcul distribué) semble justifiée.

2. **Génération des recommendations**
    - Une fois l'algorithme de collaborative filtering exécuté, nous pouvons générer une liste des N meilleures recommandations pour chaque utilisateur. Cette liste contiendrait les chansons qu'un utilisateur n'a pas encore écoutées mais qui sont fortement appréciées par des utilisateurs similaires.

3. **Stockage des recommendations**
    - Les recommandations générées peuvent être archivées sous forme de fichiers CSV dans notre data lake.
    - Ces recommandations peuvent également être mises en production en créant une nouvelle table dans notre base de données PostgreSQL en production. Cette table contiendrait les colonnes suivantes :

        - `user_id` : l'identifiant de l'utilisateur.
        - `track_id` : l'identifiant de la chanson recommandée.
        - `recommendation_score` : le score associé à la recommandation.
        - `created_at` : date de création de la recommendation.

4. **Servir les recommendations**
    - Enfin, nous pouvons modifier notre API afin qu'elle expose les recommandations aux utilisateurs en se basant sur la table créée.

### Étape 7

1. **Déclenchement du réentraînement du modèle**
    - Il est possible de choisir de réentraîner notre modèle à des intervalles de temps fixes après avoir reçu chaque batch de données. Cependant, cela n'est pas optimal. Si le nouveau batch de données est peu significatif par rapport au volume total des données, les recommandations risquent de ne pas beaucoup évoluer.
    - Une alternative serait de réentraîner le modèle lorsque un seuil de nouvelles données est atteint après avoir reçu un batch. Cela garantirait que les recommandations sont sensiblement mises à jour en fonction des nouveaux comportements des utilisateurs.
    - Il serait pertinent de hiérarchiser les recommandations en fonction de leur date de création et de leur score, afin de privilégier les recommandations récentes et pertinentes.

2. **Modification des recommendations**
    - Les nouvelles recommandations peuvent être ajoutées à la table de recommandations dans notre base de données en production.
    - On pourrait alors hiérarchiser les recommendations en fonction de leur date de création et de leur score.

3. **Amélioration et feedback utilisateur**
    - À ce stade, nous pourrions mettre en place un système d’analytique pour évaluer et suivre l’évolution des performances du système de recommandations en fonction de l’engagement des utilisateurs :
        - Suivi des KPI importants par rapport aux objectifs business.
        - Nombre de chansons recommandées qui ont été écoutées.
        - Nombre de chansons recommandées passées.
        - Mise en place d’un mécanisme permettant aux utilisateurs de signaler s’ils apprécient les recommandations (e.g., boutons "J’aime", "Je n’aime pas").
    - Ces métriques permettraient de guider les futures évolutions du système de recommandations en identifiant les points d'amélioration.