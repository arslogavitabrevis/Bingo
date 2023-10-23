from custom_types import COMMANDES, BASE_DONNE, CARTE, RetourCommande
from typing import List
from pdflatex import PDFLaTeX
from datetime import datetime
from math import floor
from random import random


class PdfCreator:

    @classmethod
    def gestionnaire_commande(cls, commandes: COMMANDES, base_donnée: BASE_DONNE):
        nombres_cartes = [c.nombre_cartes for c in commandes]
        date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        fichier_pdfs: List[RetourCommande] = []
        for i, commande in enumerate(commandes):

            file_name = "cartes_pdf/creation_carte_pdf/_temp.tex"
            with open(file_name, "wb") as f:
                idx_carte = -1*sum(nombres_cartes[i:])
                if idx_carte == -1*nombres_cartes[i]:
                    bd_simplifié = base_donnée[idx_carte:]
                else:
                    bd_simplifié = base_donnée[idx_carte:idx_carte +
                                               nombres_cartes[i]]
                f.write(cls.__create_latex_string(
                    commande.nom_client, commande.nombre_cartes, bd_simplifié).encode())

            with open(file_name, 'rb') as f:
                chemin_fichier_pdf = f"cartes_pdf/{commande.nom_client}{date}"
                pdfl = PDFLaTeX.from_binarystring(f.read(), chemin_fichier_pdf)

                pdf, log, completed_process = pdfl.create_pdf(
                    keep_pdf_file=True, keep_log_file=False)
            fichier_pdfs.append(
                RetourCommande(
                    commande=commande, fichier_pdf=chemin_fichier_pdf))

        return fichier_pdfs

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
\\usepackage{{xcolor}}
\\usepackage{{tabularray}}
\\usepackage[margin=0.5in]{{geometry}}

\\title{{BINGO  {{\\Huge Énergi-sant!}}}}
\\begin{{document}}

\\maketitle
\\huge
\\begin{{center}}
Cartes de {}

{}
\\end{{center}}
\\end{{document}}""".format(nom_client, PdfCreator.__remplisseur_cartes(cartes))

    @staticmethod
    def __remplisseur_cartes(cartes: List[CARTE]) -> str:
        cartes_tex = [PdfCreator.__remplisseur_carte(
            carte) for carte in cartes]
        ligne_carte_tex = [" ".join((cartes_tex[i*2], cartes_tex[i*2+1]))
                           for i in range(floor(len(cartes_tex)/2))]
        if len(cartes_tex) % 2 != 0:
            ligne_carte_tex.append(cartes_tex[-1])

        return "\n\n".join(ligne_carte_tex)

    @staticmethod
    def __remplisseur_carte(carte: CARTE) -> str:
        numéro = [numero for _, numeros in carte
                  for numero in numeros]

        couleurs = ["blue", "red", "green", "cyan", "magenta", "yellow",
                    "lime", "olive", "orange", "pink", "purple", "teal", "violet",]
        couleur_choisies = [couleurs.pop(round(random()*len(couleurs))-1)
                            for i in range(len("BINGO"))]
        return """\\begin{{tblr}}{{
    hlines={{0.7pt, solid}}, vlines={{0.7pt, solid}},
    hline{{2-Y}} = {{0.5pt, solid}},
    colspec={{ccccc}}, rows={{18mm}}, columns={{18mm}},
    rowsep=0mm, colsep=0mm, stretch=0mm,
}}
\\SetCell{{{24}!{trs}}}{{\\Huge B \\par}} & \\SetCell{{{25}!{trs}}}{{\\Huge I \\par}} & \\SetCell{{{26}!{trs}}}{{\\Huge N \\par}} & \\SetCell{{{27}!{trs}}}{{\\Huge G \\par}} & \\SetCell{{{28}!{trs}}}{{\\Huge O \\par}} \\\\
 {0} & {5} & {10} & {14} & {19} \\\\
 {1} & {6} & {11} & {15} & {20} \\\\
 {2} & {7} & \\SetCell{{blue!25}}{{\\Large Gratuit \\par}} & {16} & {21} \\\\
 {3} & {8} & {12} & {17} & {22} \\\\
 {4} & {9} & {13} & {18} &  {23}    
\end{{tblr}}""".format(*numéro, *couleur_choisies, trs=55)
