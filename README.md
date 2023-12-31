# Piece of Mind (Django Edition)

## Configuration
Distribution
 - Python 3.11.6

Librairies nécessaires
- django 4.2.6
- djangorestframework 3.14.0
- rsa 4.9
- pyjwt 2.8.0
- base64 (implémentée de base dans la distrib python)

## Exploitation du projet

### Démarrer le serveur django (depuis un terminal)
Installer la version de python précisée au début de cette documentation

Cloner le repository
```shell
git clone ssh/https....
```
Ne pas rentrer dans le directory directement

#### Créer un environnement virtuel
```shell
python -m venv djangoEnv
```
##### Activer l'environnement virtuel
#### Windows
```
djangoEnv\Scripts\activate
```

#### Linux
```
source djangoEnv/bin/activate
```
##### Installer les librairies nécessaires
```
cd POM_API
python -m pip install -r requirements.txt
```

##### Démarrer le serveur
```
python manage.py runserver
```

## ROADMAP

### FINI
#### Users
- Encodage du mot de passe avant de le mettre en DB (avec une clé public et on jette la clé privé, bon on l'a gardé au cas , elle changera plus tard)
- Modification d'un mot de passe utilisateur (lorsqu'il envoie le jwt pour assurer qu'il est bien authentifié)

#### Token
- Génération de Tokens 
- Ajouter une vérification par signature des (vérifier la secret key avec la signature du token envoyé)
- Ajout d'une vérification que l'email de la requete est bien présente dans le token (après son decodage avec la clé privée)

### TO DO
#### Users
- Suppression d'un utilisateur
- Mettre une sécurité sur les usernames, email, avec du regex

#### Messages
- Créer le model de messages (localisation, contenu, likes etc...)
- Requetes création, supression, ajout like, suppression like
- Requete get tout les messages sur un radius de x distance sur une position donnée

#### Données
- Gérer la connexion avec un réelle bas de données PostGreSQL et non celle implémentée par Django

#### Documentations
- Commencer à rédiger une doc propres des différentes méthodes de l'API (possiblement un markdown quelque part)