import yagmail
from custom_types import RetourCommande
import json
from typing import Dict


class EmailSender:
    def __init__(self, fichier_parametres="email_sender_param.json"):
        with open(fichier_parametres, "r")as f:
            param: Dict = json.load(f)
            
        self.__courriel_reference = param["courriel_reference"]
        self.yag = yagmail.SMTP(param["courriel_principal"], param["mot_de_passe"])

    def envoyer_email(self, retour_commande: RetourCommande):
        contents = ["""Bonjour {},

Nous vous remercions pour votre don de {} $ à centraide. Vous trouverez en pièce jointe vos {} cartes de bingo!

Bonne chance!

L\'équipe du Bingo Énergi-sant""".format(
            retour_commande.commande.nom_client,
            retour_commande.commande.montant_don,
            retour_commande.commande.nombre_cartes,
        )]

        self.yag.send(to=[retour_commande.commande.adressse_courriel],
                      subject='Vos cartes de bingo Énergi-sant!',
                      cc=[self.__courriel_reference],
                      contents=contents,
                      attachments=retour_commande.fichier_pdf)
