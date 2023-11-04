from typing import Dict, List, Tuple
import json
import pickle
from custom_types import BASE_DONNE, COMMANDES, Commande, CARTE
import pandas as pd
from datetime import datetime

class VerificationCartes:
    
    CHEMIN_SAUVEGARDE = "cartes_crees/base_données_cartes.pkl"
    DEBUG = False
    
    def __init__(self, fichier_numéros="numéro_tirés.json"):
        date = datetime.now().strftime('%Y-%m-%d')
        # Ouvrir le fichier de numéros
        with open(fichier_numéros, "r")as f:
            raw_number:  Dict[str,List[int]] = json.load(f)
            self.nums = set(raw_number["numéros"])

        # Ouvrir la base de données des cartes sauvegardées
        with open(self.CHEMIN_SAUVEGARDE, "rb") as f:
            self.base_données: BASE_DONNE = pickle.load(f)
        
        self.__compteur_cartes:Dict[Commande, int] = {}
        self.__ranking:Dict[str,int] = {}
    
        for entree in self.base_données:
            self.vérification_client(entree)
        noms, score = list(zip(*sorted(list(self.__ranking.items()),key=lambda x:x[1], reverse=True)))
        pd.options.display.float_format = '${:,.2f}'.format
        pd.DataFrame({"Participant":noms,"Nombre numéro gagnant":score}).to_csv(f"Résultats {date}.csv")
 
    
    def vérification_client(self,entre_bd:Tuple[Commande, CARTE]):
        commande, carte = entre_bd
        
        if commande not in self.__compteur_cartes.keys():
            self.__compteur_cartes[commande] = 1
        else:
            self.__compteur_cartes[commande] += 1
        
        if self.vérification_carte(carte, commande.nom_client):
            print(f"{commande.nom_client} est gagnant pour carte #{self.__compteur_cartes[commande]}!!!!")
        
    def vérification_carte(self,carte:CARTE, nom:str):
        #Tuple[Tuple[str, Tuple[int]],...]
        numéro_sortis = [numéro in self.nums 
            for lettre, numéros in carte
            for numéro in numéros ]
        count = numéro_sortis.count(True) 
        try:
            self.__ranking[nom] = max(self.__ranking[nom],count/len(numéro_sortis))
        except KeyError:
            self.__ranking[nom] = count/len(numéro_sortis)
        
        if self.DEBUG:    
           print(f"{nom} a {count} numéro gagnant sur {len(numéro_sortis)}")
        
        return all(numéro_sortis)
            
VerificationCartes()