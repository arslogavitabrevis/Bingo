from custom_types import COMMANDE, BASE_DONNE, CARTE
from typing import List
from pdflatex import PDFLaTeX
import os
from datetime import datetime
import shutil
from time import sleep
from math import floor


class PdfCreator:

    @classmethod
    def gestionnaire_commande(cls, commandes: COMMANDE, base_donnée: BASE_DONNE):
        clients, nombres_cartes = zip(*commandes)
        date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        for i, commande in enumerate(commandes):
            client, nb = commande
            
            file_name = "cartes_pdf/creation_carte_pdf/_temp.tex"
            with open(file_name, "wb") as f:
                idx_carte = -1*sum(nombres_cartes[i:])
                if idx_carte == -1*nombres_cartes[i]:
                    bd_simplifié = base_donnée[idx_carte:]
                else:
                    bd_simplifié = base_donnée[idx_carte:idx_carte +
                                            nombres_cartes[i]]
                f.write(cls.__create_latex_string(
                    client, nb, bd_simplifié).encode())
                
            with open(file_name, 'rb') as f:
                pdfl = PDFLaTeX.from_binarystring(f.read(), f"cartes_pdf/{client}{date}")

                pdf, log, completed_process = pdfl.create_pdf(
                keep_pdf_file=True, keep_log_file=False)
                

            # shutil.copy(f"{file_name.split('.')[0]}.pdf",f"cartes_pdf/{client}{date}.pdf")

    @staticmethod
    def __create_latex_string(nom_client: str, nombre_carte: int, base_donnée: BASE_DONNE) -> str:
        # Vérifier le contenu de la base de donnée:
        if len(base_donnée) != nombre_carte:
            ValueError(
                "Nombre de carte incorrect dans la base de donnée simplifiée")

        noms_clients, cartes = zip(*base_donnée)

        if len(noms_clients) != 1 or nom_client not in noms_clients:
            ValueError(
                "Nom du client incorrect dans la base de donnée simplifiée")

        return """\\documentclass{{article}}
\\usepackage[thinlines]{{easytable}}
\\usepackage[margin=0.5in]{{geometry}}

\\title{{Cartes de BINGO de {}}}
\\begin{{document}}

\\maketitle
\\huge
\\begin{{center}}
{}
\\end{{center}}
\\end{{document}}""".format(nom_client, PdfCreator.__remplisseur_cartes(cartes))

    @staticmethod
    def __remplisseur_cartes(cartes: List[CARTE]) -> str:
        cartes_tex = [PdfCreator.__remplisseur_carte(carte) for carte in cartes]
        ligne_carte_tex = [" ".join((cartes_tex[i*2], cartes_tex[i*2+1])) for i in range(floor(len(cartes_tex)/2))]
        if len(cartes_tex)%2 !=0:
            ligne_carte_tex.append(cartes_tex[-1])
            
        return "\n\n".join(ligne_carte_tex)

    @staticmethod
    def __remplisseur_carte(carte: CARTE) -> str:
        numéro = [numero for _, numeros in carte
                  for numero in numeros]
        return """\\begin{{TAB}}(e,1.6cm,1.6cm){{|c:c:c:c:c|}}{{|c|c:c:c:c:c|}}
{{\\Huge B \\par}} & {{\\Huge I \\par}} & {{\\Huge N \\par}} & {{\\Huge G \\par}} & {{\\Huge O \\par}} \\\\
 {0} & {5} & {10} & {14} & {19} \\\\
 {1} & {6} & {11} & {15} & {20} \\\\
 {2} & {7} & {{\\Large Gratuit \\par}} & {16} & {21} \\\\
 {3} & {8} & {12} & {17} & {22} \\\\
 {4} & {9} & {13} & {18} &  {23}   
\end{{TAB}}""".format(*numéro)
