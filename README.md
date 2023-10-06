# Piece of Mind (Django Edition)

## Configuration
Distribution
 - Python 3.11.6

Librairies nécessaires
- django 4.2.6
- djangorestframework 3.14.0
- pycrypto (à voir)

## TO DO
### Users
- Recherche d'un user en fonction de son email, ou username
- Encodage du mot de passe avant de le mettre en DB (avec une clé public et on jette la clé privé)
- Modification d'un mot de passe
- Suppression d'un utilisateur

### Messages
- Créer le model de messages (localisation, contenu, likes etc...)
- Requetes création, supression, ajout like, suppression like
- Requete get tout les messages sur un radius de x distance sur une position donnée

### Données
- Gérer la connexion avec un réelle bas de données PostGreSQL et non celle implémentée par Django