import os
from carte_bingo import CreateurCarte
import pickle
from typing import List, Tuple


class GestionnaireCarte:
    BD_TYPE = List[Tuple[str, CreateurCarte.Carte]]

    def __init__(self) -> None:
        self.commande = []
        
        # Vérifier si le fichier de base de données de carte existe:
        if not os.path.isfile("cartes_crees/base_données_cartes.json"):
            self.base_données: GestionnaireCarte.BD_TYPE = []
            liste_clients = []
            liste_cartes = []
        else:
            # Ouvrir la base de données des cartes sauvegardées
            with open("cartes_crees/base_données_cartes.json", "rb") as f:
                self.base_données: GestionnaireCarte.BD_TYPE = pickle.load(f)
            liste_clients, liste_cartes = zip(*self.base_données)
            print(f"Il y a actuellement {len(set(liste_clients))} clients.")
            print(f"Il y a actuellement {len(liste_cartes)} cartes de bingo")
        self.set_cartes = set(liste_cartes)

        print("Bienvenu dans le créateur de cartes.\n")
        while self.demande_cartes():
            print("Les cartes seront générées seulement à la fin")

        with open("cartes_crees/base_données_cartes.json", "wb") as f:
            pickle.dump(self.base_données, f)

    def demande_cartes(self):
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
        return input("Entrer d'autre commandes?\n").lower() in {"oui", "yes", "o", "y"}


GestionnaireCarte()
