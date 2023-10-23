from typing import List, Tuple, NamedTuple

class Commande(NamedTuple):
    nom_client:str
    adressse_courriel:str
    montant_don:float
    nombre_cartes:int
    
class RetourCommande(NamedTuple):
    commande:Commande
    fichier_pdf:str

CARTE = Tuple[Tuple[str, Tuple[int]],...]
BASE_DONNE = List[Tuple[str, CARTE]]
COMMANDES = List[Commande]




    