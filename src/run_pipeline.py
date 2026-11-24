import os
from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from ner import ajouter_entites
from classifiers import charger_modele, classer_phrases, extraire_decisions_actions
from slots import remplir_infos
from topics import decouper_en_sujets, trouver_mots_cles
from summary import resumer_sujet
from report import construire_compte_rendu, sauvegarder_json, sauvegarder_markdown
from export_pdf import sauvegarder_pdf


FICHIER = "data/reunion2.txt"   # change ici pour tester une autre réunion

with open(FICHIER, encoding="utf-8") as f:
    texte_brut = f.read()

# 1) nettoyage, phrases, entités
prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)
phrases = ajouter_entites(phrases)

# 2) décisions et actions
modele = charger_modele()
phrases = classer_phrases(phrases, modele)
decisions, actions = extraire_decisions_actions(phrases)

participants = []
for prise in prises:
    if prise["speaker"] not in participants:
        participants.append(prise["speaker"])

decisions = remplir_infos(decisions, participants)
actions = remplir_infos(actions, participants)

# 3) sujets, mots-clés, résumés
prenoms = []
for nom in participants:
    prenoms.append(nom.lower())

sujets = decouper_en_sujets(phrases)
mots_cles = trouver_mots_cles(sujets, prenoms)

resumes = []
for sujet in sujets:
    resumes.append(resumer_sujet(sujet))

# 4) assemblage et export
cr = construire_compte_rendu("Compte rendu de réunion", participants,
                             mots_cles, resumes, decisions, actions)

os.makedirs("output", exist_ok=True)
sauvegarder_json(cr, "output/compte_rendu.json")
sauvegarder_markdown(cr, "output/compte_rendu.md")
sauvegarder_pdf(cr, "output/compte_rendu.pdf")

print("Terminé ! Ouvre output/compte_rendu.md")