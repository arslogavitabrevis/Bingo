from random import random
from typing import Tuple,Set
from custom_types import CARTE

class CreateurCarte:   

    @classmethod
    def nouvelle_carte(cls, base_donnes:Set[CARTE]):
        for i in range(1000):
            nouvelle_carte = cls._creer_carte()
            if  cls.verifier_si_carte_existante(base_donnes, nouvelle_carte):
                return nouvelle_carte
        raise ValueError("Nombre d'essaie pour la création d'une nouvelle carte dépassé")
            
    @staticmethod
    def _creer_carte():
        return tuple((lettre, CreateurCarte._colonne(i,lettre))
                 for i,lettre in enumerate("BINGO")) 
        
        
    @staticmethod
    def _colonne(letter_index:int,letter: str):
        """Retourne une liste de nombre à mettre dans la colonne"""
        if letter.upper() == "N":
            number_of_number = 4
        else:
            number_of_number = 5
        pool = list(range(1+(letter_index*15),1+(letter_index+1)*15))
        return tuple(pool.pop(round((len(pool)-1)*random())) for i in range(number_of_number))
    
    @staticmethod
    def verifier_si_carte_existante(base_donnees:Set[CARTE], nouvelle_carte:CARTE):
        return not nouvelle_carte in base_donnees

