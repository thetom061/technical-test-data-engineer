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

Base de données relationelle (SQL) - données hautement relationelle + schéma simple qui ne risque pas de changer si on choisit une autre méthode on perd de la performance sur nos queries d'Aggrégation ou de join. Problème si on scale avec beaucoup d'utilisateurs qui commencent à utiliser notre application (sharding ou replication peut alors être utilisé) et dans ce cas la vu que nosql scale mieux on pourrait réfléchir à changer.

### Étape 5

_votre réponse ici_

### Étape 6

ALS collaborative filtering.

### Étape 7

_votre réponse ici_
