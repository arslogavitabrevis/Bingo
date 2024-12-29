from typing import Dict, List, Tuple, NamedTuple,cast
import json
import pickle
from custom_types import BASE_DONNE, COMMANDES, Commande, CARTE
import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np


class VerificationCartes:

    class SuiviParticipant(NamedTuple):
        nom_participant: str
        nombre_numero: int
        numéro_carte: int
        gagnant:bool
        numéro_manquants:List[int]

    CHEMIN_SAUVEGARDE = "cartes_crees/base_données_cartes.pkl"
    DEBUG = False

    def __init__(self, numéros: List[int], numéro_par_jour:int, jour: int = None):
        top = 7
        if jour == None:
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = f"Jour {jour}"
        print(f"Analyse du {date}")
        
        dossier_resultats = Path("Résultats")
        dossier_resultats.mkdir(parents=True, exist_ok=True)
        # Ouvrir le fichier de numéros
        self.nums = numéros

        # Ouvrir la base de données des cartes sauvegardées
        with open(self.CHEMIN_SAUVEGARDE, "rb") as f:
            self.base_données: BASE_DONNE = pickle.load(f)

        self.__compteur_cartes: Dict[Commande, int] = {}
        self.__ranking: Dict[str, VerificationCartes.SuiviParticipant] = {}

        for entree in self.base_données:
            self.vérification_client(entree)
        noms, score, numéro_carte, gagnants, num_manquants = list(
            zip(*sorted(list(self.__ranking.values()), key=lambda x: x.nombre_numero, reverse=True)))
        pd.options.display.float_format = '${:,.2f}'.format
        pd.DataFrame({"Participant": noms, 
                      "Nombre de numéro gagnant": score, 
                      "Carte la plus avancée":numéro_carte,
                      "Numéros_manquants":num_manquants,}).to_csv(
            dossier_resultats/f"Résultats {date}.csv", index=False)

        print("Top {}: \n\t{}".format(top,
                                      "\n\t".join([f"{nm}: {sc}" for nm, sc in zip(noms[0:top], score[0:top])])))

        if cast(List[bool],gagnants).count(True) > 1 and numéro_par_jour >1:
            for i in reversed(range(numéro_par_jour)):
                VerificationCartes(numéros[:-i],
                                   1,
                                   jour=f"{jour} numéro #{numéro_par_jour-i}")

    def vérification_client(self, entre_bd: Tuple[Commande, CARTE]):
        commande, carte = entre_bd

        if commande not in self.__compteur_cartes.keys():
            self.__compteur_cartes[commande] = 1
        else:
            self.__compteur_cartes[commande] += 1

        self.vérification_carte(carte, commande.nom_client, self.__compteur_cartes[commande])
        # if self.vérification_carte(carte, commande.nom_client, self.__compteur_cartes[commande]):
        #     print(
        #         f"{commande.nom_client} est gagnant pour carte #{self.__compteur_cartes[commande]}!!!!")

    def vérification_carte(self, carte: CARTE, nom: str, numéro_carte: int):
        # Tuple[Tuple[str, Tuple[int]],...]
        if "Marie" in nom:
            pass  
        numéro_de_la_carte = [numéro for lettre, numéros in carte
                         for numéro in numéros]
        numéro_sortis = [numéro in self.nums
                         for numéro in numéro_de_la_carte]
        count = numéro_sortis.count(True)
        gagnant =  count/len(numéro_sortis) == 1
        numéro_manquants = [n for n, c in zip(numéro_de_la_carte, numéro_sortis)
                            if not c]
        try:
            if self.__ranking[nom].nombre_numero < count:
                self.__ranking[nom] = self.SuiviParticipant(
                    nom_participant=nom,
                    nombre_numero=count,
                    numéro_carte=numéro_carte,
                    gagnant = gagnant,
                    numéro_manquants=numéro_manquants)
        except KeyError:
            self.__ranking[nom] = self.SuiviParticipant(
                nom_participant=nom,
                nombre_numero=count,
                numéro_carte=numéro_carte,
                gagnant = gagnant,
                numéro_manquants=numéro_manquants)

        if self.DEBUG:
            print(f"{nom} a {count} numéro gagnant sur {len(numéro_sortis)}")

        return all(numéro_sortis)


if __name__ == "__main__":
    with open("numéro_tirés.json", "r")as f:
        numéros:  Dict[str, List[List[int]]] = json.load(f)


    for jour in range(1,len(numéros)):
        VerificationCartes(numéros=[n
                                    for nums in numéros[:jour]
                                    for n in nums], 
                           numéro_par_jour=  len(numéros[jour]),
                           jour=str(jour))
