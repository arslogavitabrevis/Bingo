import pandas as pd
from gestionnaire_cartes import GestionnaireCarte

gestionnnaire_cartes = GestionnaireCarte()

participants = list({commande.nom_client for commande in  gestionnnaire_cartes.liste_commandes_précédentes})
print(f"Nombre de participants: {len(participants)} ")
courriels =  [gestionnnaire_cartes.touver_courriel.pattern_adresse_courriel(participant)
for participant in participants]
pd.DataFrame({"Participants":participants,
             "Courriels":courriels,}).to_csv("Liste participants.csv")

with open("courriel_agrégé.txt","w") as f:
    f.write(";".join(courriels))


