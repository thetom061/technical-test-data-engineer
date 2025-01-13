# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

### **Environnement de Test**
- **Version de Python** : 3.10.8
- **Environments testés**: MacOs, linux

### Contexte

Cette partie vise à expliquer les choix techniques fait dans la réalisation de la solution. \
En terme d'environnement virtuelle, j'ai choisi venv pour privilégier la simplicité. J'aurai pu me tourner vers des méthodes de virtualisation tel que docker ou des solutions préconfigurés tel que conda mais cela aurait rajouter de la complexité ainsi que de nouvelles dépendences sans pour autant ajouter quelque chose d'intéressant à la solution. \
Toutefois, si il avait été demandé de charger les données en base de données après extraction et transformation, l'utilisation de docker pour automatiser le déploiment de l'infrastructure aurait été justifier. En effect, ça aurait énormement réduit le temps pour reproduire et configurer l'environnement de travail au complet.



### Création et activation de l'environment virtuel


Création de  l'environment virtuelle\
`python3 -m venv venv`

On doit ensuite activer l'environmnent. \
`source venv/bin/activate`  # Sur macOS/Linux \
`.\venv\Scripts\activate`   # Sur Windows

Pour installer les dépendance nécessaires pour le projet \
`pip3 install -r requirements.txt`

On peut désactiver l'environnement en utilisant la commande \
`deactivate`

### Roulement des tests

Pour rouler les tests, il faut se placer à la racine du projet et lancer la commande \
`pytest`

Si on a une erreur **ModuleNotFoundError: No module named 'src'** \
`PYTHONPATH=$(pwd) pytest`


## Questions (étapes 4 à 7)

### Étape 4

_votre réponse ici_

### Étape 5

_votre réponse ici_

### Étape 6

_votre réponse ici_

### Étape 7

_votre réponse ici_
