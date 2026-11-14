from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from ner import ajouter_entites
from classifiers import charger_modele, classer_phrases, extraire_decisions_actions
from slots import remplir_infos

with open("data/reunion2.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)
phrases = ajouter_entites(phrases)

modele = charger_modele()
phrases = classer_phrases(phrases, modele)
decisions, actions = extraire_decisions_actions(phrases)

# La liste des participants = les noms de ceux qui parlent
participants = []
for prise in prises:
    if prise["speaker"] not in participants:
        participants.append(prise["speaker"])

decisions = remplir_infos(decisions, participants)
actions = remplir_infos(actions, participants)

print("Participants :", participants)

print("\n=== DÉCISIONS ===")
for d in decisions:
    print("-", d["text"])
    print("    échéance :", d["deadline"])

print("\n=== ACTIONS ===")
for a in actions:
    print("-", a["text"])
    print("    responsable :", a["responsible"])
    print("    échéance    :", a["deadline"])