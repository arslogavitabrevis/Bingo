from difflib import get_close_matches


class AdresseCourriel:
    
    __FICHIERLISTECOURRIEL = "liste_courriel.csv"
    __DOMAINE_PRINCIPAL = "@domain1.com"
    __DOMAINE_SECONDAIRE = "@domain2.com"
    def __init__(self) -> None:
        with open(self.__FICHIERLISTECOURRIEL, "r") as f:
            self.liste_courriels = set(f.read().split("\n"))
    
    def pattern_adresse_courriel(self, prénom_nom:str):
        prénom,nom = prénom_nom.split(" ")
        return f"{self.__pattern_economie(prénom, nom)};{prénom.lower()}.{nom.lower()}{self.__DOMAINE_SECONDAIRE};"

    def __pattern_economie(self, prénom:str, nom:str):
        essaie = f"{prénom.lower()}.{nom.lower()}{self.__DOMAINE_PRINCIPAL}"
        if essaie not in self.liste_courriels:
           match = get_close_matches(essaie, self.liste_courriels)
           if len(match) == 0:
               raise ValueError(f"Aucune adresse courriel correspondante pour {prénom} {nom}")
           elif len(match) ==1:
               print(f"Une seule adresse de correspondance pour {prénom} {nom}")
               return match[0]
           elif len(match) >1:
               choix = "\n\t".join([f"{i} : {adr}" for i, adr in enumerate(match)])
               return match[int(input(f"Choisir l'adresse pour {prénom} {nom}{chr(10)}{chr(9)}{choix}{chr(10)}"))][1:-1]
        else:
            return essaie 
    
    