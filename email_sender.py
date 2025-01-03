import yagmail
from custom_types import RetourCommande
import json
from typing import Dict


class EmailSender:
    def __init__(self, fichier_parametres="email_sender_param.json"):
        with open(fichier_parametres, "r")as f:
            param: Dict = json.load(f)

        self.__courriels_references = param["courriels_references"]
        self.yag = yagmail.SMTP(
            param["courriel_principal"], oauth2_file='oauth2_creds.json')

    def envoyer_email(self, retour_commande: RetourCommande):
        contents = ["""Bonjour {},

Nous vous remercions pour votre don de {} $ à la campagne Entraide. Vous trouverez en pièce jointe vos {} cartes de bingo!

Bonne chance!

L\'équipe du Bingo Énergi-sant, Claudia Dupont, Josélie Bégin, Julie Poulin, Mathieu Trudelle, Maude Grenier-Hamel, Raphaël Grenier""".format(
            retour_commande.commande.nom_client,
            retour_commande.commande.montant_don,
            retour_commande.commande.nombre_cartes,
        )]
        adresses = [adr for adr in retour_commande.commande.adressse_courriel.split(";")
                    if adr != ""]
        self.yag.send(to=adresses,
                      subject='Vos cartes de bingo Énergi-sant!',
                      cc=self.__courriels_references,
                      contents=contents,
                      attachments=retour_commande.fichier_pdf)
