import os
from carte_bingo import CreateurCarte
import pickle
from prettytable import PrettyTable
from datetime import datetime
from custom_types import BASE_DONNE, COMMANDES, Commande, CARTE
from jolie_pdf import PdfCreator
from email_sender import EmailSender
from typing import List, Tuple
from copy import deepcopy
import pandas as pd
import shutil
from pattern_adresse_courriel import AdresseCourriel
from pathlib import Path


class GestionnaireCarte:
    OUI = {"oui", "yes", "o", "y"}

    def __init__(self) -> None:
        self.commande: COMMANDES = []
        self.date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        # Vérifier si le fichier de base de données de carte existe:
        dossier_sauvegarde = Path("cartes_crees")
        dossier_sauvegarde.mkdir(parents=True, exist_ok=True)
        self.fichier_sauvegarde = dossier_sauvegarde/"base_données_cartes.pkl"
        
        if not os.path.isfile(self.fichier_sauvegarde):
            self.base_données: BASE_DONNE = []
            self.liste_commandes_précédentes: List[Commande] = []
            liste_cartes: List[CARTE] = []
        else:
            # Ouvrir la base de données des cartes sauvegardées
            with open(self.fichier_sauvegarde, "rb") as f:
                self.base_données: BASE_DONNE = pickle.load(f)
            self.liste_commandes_précédentes, liste_cartes = zip(*self.base_données)
            clients = set(
                [commande_précédente.nom_client for commande_précédente in self.liste_commandes_précédentes])
            print(f"Il y a actuellement {len(clients)} clients.")
            print(f"Il y a actuellement {len(liste_cartes)} cartes de bingo")
        self.set_cartes = set(liste_cartes)

        print("Bienvenu dans le créateur de cartes.\n")

        # Définir  le nom du dossier pour les cartes
        self.__dossier_csv = "commande"
        
        # Charger la liste des email:
        self.touver_courriel = AdresseCourriel()
        
        # Partie pour faire des demande de carte manuellement
        # while self.demande_cartes_manuel():
        #     print("Les cartes seront générées seulement à la fin")
    
    def passer_commande(self):
        # Pour faire des demande de carte depuis le CSV
        self.lecture_csv_entre()

        # Enregistrement de la commande dans la base de donnée
        pt = PrettyTable(field_names=(
            "Nom client", "Adressse Courriel", "Montant Don", "Nombre Cartes"))
        pt.add_rows(self.commande)
        if input("La commande est-elle valide?\n{}\n".format(pt)).lower() in GestionnaireCarte.OUI:
            
            print("Création des carte en format pdf")
            retour_commandes = PdfCreator.gestionnaire_commande(
                self.commande, self.base_données)

            print("Envois des courriels")
            self.email_sender = EmailSender()
            for retour_commande in retour_commandes:
                self.email_sender.envoyer_email(retour_commande)
            self.archiver_comande()
            print("Envois Complété")
            
            # Faire un enregistrement de sauvegarde
            with open(f"{self.fichier_sauvegarde.stem}_{self.date}.{self.fichier_sauvegarde.suffix}", "wb") as f:
                pickle.dump(self.base_données, f)
            with open(self.fichier_sauvegarde, "wb") as f:
                pickle.dump(self.base_données, f)
            print("Commande sauvegardée")
        else:
            print("Commande annulée")
            return
    
    def ajout_cartes(self, commande, nombre_cartes):
        for i in range(nombre_cartes):
            self.base_données.append(
                (commande, CreateurCarte.nouvelle_carte(self.set_cartes)))

    def demande_cartes_manuel(self):
        """Gestion d'une commande individuelle de carte"""
        try:
            nom_client = input("Entrer le nom du client:\n")
            montant_don = int(
                input("Entrez le montant du don:\n"))
        except KeyboardInterrupt:
            continuer = print("\nEntrée annulée.")
            return False
        nombre_cartes = self.conversion_don_nombre_cartes(montant_don)
        commande = Commande(
            nom_client=nom_client,
            adressse_courriel=self.touver_courriel.pattern_adresse_courriel(nom_client),
            montant_don=montant_don,
            nombre_cartes=nombre_cartes)
        self.commande.append(commande)
        self.ajout_cartes(commande, nombre_cartes)
        return True

    def ouvrir_fichier_commande(self)-> pd.DataFrame:
        return pd.read_csv(
            f"{self.__dossier_csv}/{self.__fichier_csv_commande}")

    def lecture_csv_entre(self):
        # Ouvrir le fichier csv

        self.__fichier_csv_commande = "commande.csv"

        commande_csv = self.ouvrir_fichier_commande()

        # Ajouter les commandes
        for i, row in commande_csv.iterrows():
            nom_participant:str = row["Nom client"]
            
            #Enlever les accents pour éviter que ça crée des bug à l'envois du courriel
            for c in "éÉÈèëËêÊ":
                if c in nom_participant:
                    print(f"Le caractère {c} a été enlevé du nom {nom_participant}")
                    nom_participant = nom_participant.replace(c, "e")                    
                 
            montant_don = row["Montant don"]
            adresse_courriel = self.touver_courriel.pattern_adresse_courriel(nom_participant)
            nombre_cartes = self.conversion_don_nombre_cartes(montant_don)
            commande = Commande(nom_client=nom_participant,
                                adressse_courriel=adresse_courriel,
                                montant_don=montant_don,
                                nombre_cartes=nombre_cartes)
            self.commande.append(commande)
            self.ajout_cartes(commande, nombre_cartes)

    def archiver_comande(self):
        # Sauvegarder le document
        toute_les_commandes = Path(f"{self.__dossier_csv}/archive/toute_les_commandes.csv")
        if not os.path.isfile(toute_les_commandes):
            toute_les_commandes.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(f"{self.__dossier_csv}/modele.csv",
                        toute_les_commandes)

        bd_csv_commandes = pd.read_csv(toute_les_commandes)

        commande_csv = pd.read_csv(
            f"{self.__dossier_csv}/{self.__fichier_csv_commande}")
        nouvelle_bd: pd.DataFrame = pd.concat([bd_csv_commandes, commande_csv])
        montant_total = nouvelle_bd["Montant don"].sum()
        print(f"Le montant total amassé est de {montant_total} $.")

        os.rename(f"{self.__dossier_csv}/{self.__fichier_csv_commande}",
                  f"{self.__dossier_csv}/archive/{Path(self.__fichier_csv_commande).stem}{self.date}.csv")

        nouvelle_bd.to_csv(toute_les_commandes)
        shutil.copy(toute_les_commandes,
                    f"{self.__dossier_csv}/archive/toute_les_commandes{self.date}.csv")

    @staticmethod
    def conversion_don_nombre_cartes(montant_don: float) -> int:
        montant_don_copie = deepcopy(montant_don)

        def retour_nb_carte(montant_restant, table):
            for montant, nb in table:
                if montant_restant >= montant:
                    return nb, montant
            return 0, 0

        table_prix: List[Tuple[float, int]] = sorted([
            # Prix $, Nombre de cartes
            (5, 2),
            (10, 5),
            (20, 12),
        ], key=lambda x: x[0], reverse=True)

        nb_cartes = 0
        for i in range(500):
            nb_carte_ajouter, montant_a_enlever = retour_nb_carte(
                montant_don_copie, table_prix)
            nb_cartes += nb_carte_ajouter
            montant_don_copie -= montant_a_enlever

            if montant_don_copie == 0:
                return nb_cartes

            if montant_don_copie != 0 and nb_carte_ajouter == 0:
                print("Résidut de {} $ sur le don".format(montant_don_copie))
                return nb_cartes

            if montant_don_copie < 0:
                raise ValueError(
                    "Erreur à déterminer le nombre de cartes: montant négatif")

        if i >= 1000:
            raise ValueError("Erreur à déterminer le nombre de cartes")



if __name__ == "__main__":
    gestionnaire_cartes = GestionnaireCarte()
    gestionnaire_cartes.passer_commande()

