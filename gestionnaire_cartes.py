import os
from carte_bingo import CreateurCarte
import pickle
from typing import List, Tuple
from prettytable import PrettyTable
from datetime import datetime


class GestionnaireCarte:
    BD_TYPE = List[Tuple[str, CreateurCarte.Carte]]
    OUI = {"oui", "yes", "o", "y"}
    CHEMIN_SAUVEGARDE = "cartes_crees/base_données_cartes.pkl" 

    def __init__(self) -> None:
        self.commande = []

        # Vérifier si le fichier de base de données de carte existe:
        if not os.path.isfile(GestionnaireCarte.CHEMIN_SAUVEGARDE):
            self.base_données: GestionnaireCarte.BD_TYPE = []
            liste_clients = []
            liste_cartes = []
        else:
            # Ouvrir la base de données des cartes sauvegardées
            with open(GestionnaireCarte.CHEMIN_SAUVEGARDE, "rb") as f:
                self.base_données: GestionnaireCarte.BD_TYPE = pickle.load(f)
            liste_clients, liste_cartes = zip(*self.base_données)
            print(f"Il y a actuellement {len(set(liste_clients))} clients.")
            print(f"Il y a actuellement {len(liste_cartes)} cartes de bingo")
        self.set_cartes = set(liste_cartes)

        print("Bienvenu dans le créateur de cartes.\n")
        while self.demande_cartes():
            print("Les cartes seront générées seulement à la fin")

        # Enregistrement de la commande dans la base de donnée
        pt = PrettyTable(field_names=("Nom client", "Nombre de carte"))
        pt.add_rows(self.commande)
        if input("La commande est-elle valide?\n{}\n".format(pt)).lower() in GestionnaireCarte.OUI:
            # Faire un enregistrement de sauvegarde
            chemin_splité = GestionnaireCarte.CHEMIN_SAUVEGARDE.split(".")
            date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            with open(f"{chemin_splité[0]}_{date}.{chemin_splité[1]}", "wb") as f:
                pickle.dump(self.base_données, f)
            with open(GestionnaireCarte.CHEMIN_SAUVEGARDE, "wb") as f:
                pickle.dump(self.base_données, f)
            print("Commande sauvegardée")
        else:
            print("Commande annulée")

    def demande_cartes(self):
        """Gestion d'une commande individuelle de carte"""
        try:
            client = input("Entrer le nom du client:\n")
            nombre_cartes = int(
                input("Entrez le nombre de cartes à générer:\n"))
        except KeyboardInterrupt:
            continuer = input("\nEntrée annulée.")
            return False

        self.commande.append((client, nombre_cartes))
        for i in range(nombre_cartes):
            self.base_données.append(
                (client, CreateurCarte.nouvelle_carte(self.set_cartes)))
        return input("Entrer d'autre commandes?\n").lower() in GestionnaireCarte.OUI


GestionnaireCarte()
