# P9
Projet 9 : Développez une application Web en utilisant Django

Ce projet a pour but de créer une application web (LITReview) permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande. 

# Processus
## Framework : Django
Ce projet utilise le framework Django pour crée l'application Web en se basant sur le modèle  MVP (Minimum Viable Product).

## Critères 
Un utilisateur devra pouvoir :
- se connecter et s’inscrire – le site ne doit pas être accessible à un utilisateur non connecté 
- consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'il suit, classés par ordre chronologique, les plus récents en premier ; 
- créer de nouveaux tickets pour demander une critique sur un livre/article ;
- créer des critiques en réponse à des tickets ;
- créer des critiques qui ne sont pas en réponse à un ticket. Dans le cadre d'un processus en une étape, l'utilisateur créera un ticket puis un commentaire en réponse à son propre ticket ;
- voir, modifier et supprimer ses propres tickets et commentaires ; 
- suivre les autres utilisateurs en entrant leur nom d'utilisateur ;
- voir qui il suit et suivre qui il veut ;
- cesser de suivre un utilisateur. 


# Utilisation

## Création de l'environnement virtuel

Pour la mise en palce de l'environnement virtuel :

## Sur Windows :
Dans le Windows Powershell il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P9.git

### Activer l'environnement virtuel
    $ cd P9 
    $ python -m venv env 
    $ ~env\scripts\activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
Dans le répertoire qui contient manage.py dans le terminal, exécutez le programme:

    $ python manage.py migrate
    $ manage.py runserver

Puis ouvrez votre navigateur et allez sur la page suivante : http://127.0.0.1:8000/
    
----------------------------------------------
## Sur MacOS ou Linux :
Dans le terminal, il faudra cloner le git.
### Récupération du projet

    $ git clone https://github.com/erikia/P9.git

### Activer l'environnement virtuel
    $ cd P9 
    $ python3 -m venv env 
    $ source env/bin/activate
    
### Installer les modules
    $ pip install -r requirements.txt

### Executer le programme
Dans le répertoire qui contient manage.py dans le terminal, exécutez le programme:

    $ python manage.py migrate
    $ manage.py runserver

Puis ouvrez votre navigateur et allez sur la page suivante : http://127.0.0.1:8000/

