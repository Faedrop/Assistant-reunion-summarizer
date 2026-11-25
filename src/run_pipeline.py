import os
from pipeline import analyser_reunion
from report import sauvegarder_json, sauvegarder_markdown
from export_pdf import sauvegarder_pdf

FICHIER = "data/reunion2.txt"   # change ici pour tester une autre réunion

with open(FICHIER, encoding="utf-8") as f:
    texte_brut = f.read()

cr, phrases = analyser_reunion(texte_brut)

os.makedirs("output", exist_ok=True)
sauvegarder_json(cr, "output/compte_rendu.json")
sauvegarder_markdown(cr, "output/compte_rendu.md")
sauvegarder_pdf(cr, "output/compte_rendu.pdf")

print("Terminé ! Ouvre le dossier output/")