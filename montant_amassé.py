import pandas as pd

# Définir  le nom du dossier pour les cartes
dossier_csv = "commande"

toute_les_commandes = f"{dossier_csv}/archive/toute_les_commandes.csv"

bd_csv_commandes = pd.read_csv(toute_les_commandes)

montant_total = bd_csv_commandes["Montant don"].sum()


print(f"Montant total: {montant_total}$")