from difflib import get_close_matches
import pathlib

class AdresseCourriel:
    
    __FICHIERLISTECOURRIEL = "liste_courriel.csv"
    __DOMAINE_COURRIEL = "@economie.gouv.qc.ca"

    def __init__(self) -> None:
        if (pathlib.Path(__file__).parent/self.__FICHIERLISTECOURRIEL).is_file():
            with open(self.__FICHIERLISTECOURRIEL, "r") as f:
                self.liste_courriels = set([c.lower()[1:-1] for c in f.read().split("\n")])
        else:
            print("Le fichier de liste de botin de courriel n'est pas disponible")
            self.liste_courriels = set()
    
    def pattern_adresse_courriel(self, prénom_nom:str):
        try:
            prénom,nom = prénom_nom.split(" ")
        except ValueError:
            raise ValueError(f"Nom de famille composé pour {prénom_nom}")
        return f"{self.__pattern_economie(prénom, nom)};"

    def __pattern_economie(self, prénom:str, nom:str):
        essaie = f"{prénom.lower()}.{nom.lower()}{self.__DOMAINE_COURRIEL}"
        if list(self.liste_courriels).count(essaie) != 1:
           if len(self.liste_courriels) == 0:
               Warning("Liste de courriel vide, les courriels pourrait être envoyé à des adresses non valides.")
               print("\tAdresse supposée:{}".format(essaie))
               if input("\tEnvoyer quand même? (Oui/Non) ") =="Oui":
                   return essaie
           match = get_close_matches(essaie, self.liste_courriels)
           if len(match) == 0:
               raise ValueError(f"Aucune adresse courriel correspondante pour {prénom} {nom}")
           elif len(match) ==1:
               print(f"Une seule adresse de correspondance pour {prénom} {nom}")
               return match[0]
           elif len(match) >1:
               choix = "\n\t".join([f"{i} : {adr}" for i, adr in enumerate(match)])
               return match[int(input(f"Choisir l'adresse pour {prénom} {nom}{chr(10)}{chr(9)}{choix}{chr(10)}"))]
        else:
            return essaie 
    
    