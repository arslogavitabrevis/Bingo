import pandas as pd
from pathlib import Path

# Définir  le nom du dossier pour les cartes

toute_les_commandes = Path(__file__).parent/"commande"/"archive"/"toute_les_commandes.csv"

if not toute_les_commandes.exists():
    toute_les_commandes.parent.mkdir(parents=True, exist_ok=True)
    tt_commande_tb = pd.concat([pd.read_csv(fichier_csv,index_col=False, delimiter=",")
                                for fichier_csv in toute_les_commandes.parent.glob("commande*")])
    tt_commande_tb.to_csv(toute_les_commandes, index=False)


bd_csv_commandes = pd.read_csv(toute_les_commandes, index_col=False)

montant_total = bd_csv_commandes["Montant don"].sum()


print(f"Montant total: {montant_total}$")
