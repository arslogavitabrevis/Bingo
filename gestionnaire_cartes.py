import os
from carte_bingo import CreateurCarte
import pickle
from prettytable import PrettyTable
from datetime import datetime
from custom_types import BASE_DONNE, COMMANDES, Commande
from jolie_pdf import PdfCreator
from email_sender import EmailSender
from typing import List, Tuple
from copy import deepcopy
import pandas as pd
import shutil


class GestionnaireCarte:
    OUI = {"oui", "yes", "o", "y"}
    CHEMIN_SAUVEGARDE = "cartes_crees/base_données_cartes.pkl"

    def __init__(self) -> None:
        self.commande: COMMANDES = []
        self.date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        # Vérifier si le fichier de base de données de carte existe:
        if not os.path.isfile(GestionnaireCarte.CHEMIN_SAUVEGARDE):
            self.base_données: BASE_DONNE = []
            liste_clients = []
            liste_cartes = []
        else:
            # Ouvrir la base de données des cartes sauvegardées
            with open(GestionnaireCarte.CHEMIN_SAUVEGARDE, "rb") as f:
                self.base_données: BASE_DONNE = pickle.load(f)
            liste_clients, liste_cartes = zip(*self.base_données)
            print(f"Il y a actuellement {len(set(liste_clients))} clients.")
            print(f"Il y a actuellement {len(liste_cartes)} cartes de bingo")
        self.set_cartes = set(liste_cartes)

        print("Bienvenu dans le créateur de cartes.\n")

        # Partie pour faire des demande de carte manuellement
        # while self.demande_cartes_manuel():
        #     print("Les cartes seront générées seulement à la fin")

        # Pour faire des demande de carte depuis le CSV
        self.lecture_csv_entre()

        # Enregistrement de la commande dans la base de donnée
        pt = PrettyTable(field_names=(
            "Nom client", "Adressse Courriel", "Montant Don", "Nombre Cartes"))
        pt.add_rows(self.commande)
        if input("La commande est-elle valide?\n{}\n".format(pt)).lower() in GestionnaireCarte.OUI:
            # Faire un enregistrement de sauvegarde
            chemin_splité = GestionnaireCarte.CHEMIN_SAUVEGARDE.split(".")
            with open(f"{chemin_splité[0]}_{self.date}.{chemin_splité[1]}", "wb") as f:
                pickle.dump(self.base_données, f)
            with open(GestionnaireCarte.CHEMIN_SAUVEGARDE, "wb") as f:
                pickle.dump(self.base_données, f)
            print("Commande sauvegardée")
        else:
            print("Commande annulée")
            return

        print("Création des carte en format pdf")
        retour_commandes = PdfCreator.gestionnaire_commande(
            self.commande, self.base_données)

        self.email_sender = EmailSender()
        for retour_commande in retour_commandes:
            self.email_sender.envoyer_email(retour_commande)
        self.archiver_comande()
        print("Envois Complété")
        
    def ajout_cartes(self, client, nombre_cartes):
        for i in range(nombre_cartes):
            self.base_données.append(
                (client, CreateurCarte.nouvelle_carte(self.set_cartes)))
            
    def demande_cartes_manuel(self):
        """Gestion d'une commande individuelle de carte"""
        try:
            client = input("Entrer le nom du client:\n")
            montant_don = int(
                input("Entrez le montant du don:\n"))
        except KeyboardInterrupt:
            continuer = print("\nEntrée annulée.")
            return False
        nombre_cartes = self.conversion_don_nombre_cartes(montant_don)
        self.commande.append(Commande(nom_client=client,
                                      adressse_courriel="",
                                      montant_don=montant_don,
                                      nombre_cartes=nombre_cartes))
        self.ajout_cartes(client, nombre_cartes)
        return True

    def lecture_csv_entre(self):
        # Ouvrir le fichier csv
        self.__dossier_csv = "commande"
        self.__fichier_csv_commande = "commande.csv"

        commande_csv = pd.read_csv(f"{self.__dossier_csv}/{self.__fichier_csv_commande}")

        # Ajouter les commandes
        for i, row in commande_csv.iterrows():
            client = row["Nom client"]
            montant_don = row["Montant don"]
            adresse_courriel = row["Adresse courriel"]
            nombre_cartes = self.conversion_don_nombre_cartes(montant_don)
            self.commande.append(Commande(nom_client=client,
                                          adressse_courriel=adresse_courriel,
                                          montant_don=montant_don,
                                          nombre_cartes=nombre_cartes))
            self.ajout_cartes(client, nombre_cartes)

    def archiver_comande(self):
        # Sauvegarder le document
        chemin_splité = self.__fichier_csv_commande.split(".")[0]
        toute_les_commandes =f"{self.__dossier_csv}/archive/toute_les_commandes.csv"
        if not os.path.isfile(toute_les_commandes):
            shutil.copy(f"{self.__dossier_csv}/modele.csv",
                  toute_les_commandes)
        
        bd_csv_commandes = pd.read_csv(toute_les_commandes)
        
        commande_csv = pd.read_csv(f"{self.__dossier_csv}/{self.__fichier_csv_commande}")
        nouvelle_bd:pd.DataFrame = pd.concat([bd_csv_commandes,commande_csv])

        os.rename(f"{self.__dossier_csv}/{self.__fichier_csv_commande}",
                  f"{self.__dossier_csv}/archive/{chemin_splité}{self.date}.csv")

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
            (3, 1),
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


GestionnaireCarte()
