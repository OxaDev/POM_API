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

## FINI
### Users
- Encodage du mot de passe avant de le mettre en DB (avec une clé public et on jette la clé privé, bon on l'a gardé au cas , elle changera plus tard)
- Modification d'un mot de passe utilisateur (lorsqu'il envoie le jwt pour assurer qu'il est bien authentifié)

### Token
- Génération de Tokens JWT

## TO DO
### Users
- Suppression d'un utilisateur

### Tokens
- Ajouter une vérification par signature des (vérifier la secret key avec la signature du token envoyé)

### Messages
- Créer le model de messages (localisation, contenu, likes etc...)
- Requetes création, supression, ajout like, suppression like
- Requete get tout les messages sur un radius de x distance sur une position donnée

### Données
- Gérer la connexion avec un réelle bas de données PostGreSQL et non celle implémentée par Django

### Documentations
- Commencer à rédiger une doc propres des différentes méthodes de l'API (possiblement un markdown quelque part)