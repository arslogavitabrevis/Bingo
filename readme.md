# Bingo

## Introduction

Ces scripts permet d'envoyer par yagmail des cartes de bingo généré automatiquement grace à pdflatex à des participant en fonction de leur don. Ensuite, il permet de valider les cartes gagnantes.


## Requis

Les instructions pour l'installation des dépendances peuvent être trouvé en ligne. 

- Python >=3.11
- pdflatex (et ses dépendances voir (https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d)
- Normalement toutes les autres dépendances devrait être intallé dans l'environnement virtuel compris dans le répertoire...

## Utilisation

1. Télécharger le répertoire git

> git clone https://github.com/arslogavitabrevis/Bingo.git

2. Remplir le fichier [email_sender_param.json](./email_sender_param.json) avec le courriel d'envois et les courriels qui seront en CC.

3. Crée un fichier d'authentification oauth2 sur la page de l'adresse d'envois [(pour gmail)](https://console.cloud.google.com/projectselector2/apis/credentials). Renommer ce fichier `oauth2_creds.json`. Le fichier d'identification est généralement valide sept jours. Au premier lancement du script avec un nouveau fichier d'identification, des instructions apparaitrons dans le terminal pour activer l'authetifiant.

4. Copier le fichier csv [modele.csv](./commande/modele.csv) et renommer la copie `commande.csv` . Inscrire les participants dans le fichier nouvellement copié.

5. Lancer le script [gestionnaire_cartes.py](./gestionnaire_cartes.py). Répondre aux questions de validation dans le terminal.  

6. L'ensemble des cartes crées sont conservées avec l'historique dans le dossier [cartes_crees](./cartes_crees). L'ensemble des cartes de bingo en format PDF crées sont conservées dans le dossier [cartes_pdf](./cartes_pdf/). Les archive des participation se trouve dans le dossier [commande/archive](./commande/archive).

7. Pour valider les cartes entrer les numéro dans le fichier [numéro_tirés.json](./numéro_tirés.json). Notez que le script a été testé avec 5 nouveau numéro tirés par jour, mais pourrait fonctionner avec un nombre de numéro tiré par jour différent. Lancer le script [vérification_cartes.py](./verification_cartes.py) et prendre connaissance des résultats dans le dossier [Résultats](./Résultats/) généré par ce script.
