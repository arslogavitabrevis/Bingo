from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

fichier_excel_comamnde = Path("commande/archive/toute_les_commandes.csv")

commandes = pd.read_csv(fichier_excel_comamnde)

commandes.sort_values(by="Date virement", inplace=True)
commandes["Montant amassé"] = commandes["Montant don"].values.cumsum()
plt.plot(commandes["Date virement"],commandes["Montant amassé"])
plt.ylabel("Montant amassé ($)")
plt.grid(which="both")
plt.show()