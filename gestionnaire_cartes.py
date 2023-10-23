import os
from carte_bingo import CreateurCarte
import pickle
from prettytable import PrettyTable
from datetime import datetime
from custom_types import BASE_DONNE, COMMANDES, Commande
from jolie_pdf import PdfCreator
from email_sender import EmailSender


class GestionnaireCarte:
    OUI = {"oui", "yes", "o", "y"}
    CHEMIN_SAUVEGARDE = "cartes_crees/base_données_cartes.pkl" 

    def __init__(self) -> None:
        self.commande:COMMANDES = []

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
        while self.demande_cartes_manuel():
            print("Les cartes seront générées seulement à la fin")

        # Enregistrement de la commande dans la base de donnée
        pt = PrettyTable(field_names=("Nom client", "Adressse Courriel", "Montant Don", "Nombre Cartes"))
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
            return
            
        print("Création des carte en format pdf")
        retour_commandes = PdfCreator.gestionnaire_commande(self.commande, self.base_données)
        
        self.email_sender = EmailSender()
        for retour_commande in retour_commandes:
            self.email_sender.envoyer_email(retour_commande)
            
        print("Envois Complété")
        
    def demande_cartes_manuel(self):
        """Gestion d'une commande individuelle de carte"""
        try:
            client = input("Entrer le nom du client:\n")
            nombre_cartes = int(
                input("Entrez le nombre de cartes à générer:\n"))
        except KeyboardInterrupt:
            continuer = print("\nEntrée annulée.")
            return False

        self.commande.append(Commande(nom_client=client,adressse_courriel="",montant_don=12,nombre_cartes=nombre_cartes))
        for i in range(nombre_cartes):
            self.base_données.append(
                (client, CreateurCarte.nouvelle_carte(self.set_cartes)))
        return True


GestionnaireCarte()
