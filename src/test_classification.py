from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from classifiers import charger_modele, classer_phrases, extraire_decisions_actions

with open("data/reunion2.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)

modele = charger_modele()
phrases = classer_phrases(phrases, modele)
decisions, actions = extraire_decisions_actions(phrases)

print("=== DÉCISIONS ===")
for d in decisions:
    print("[", d["confidence"], "]", d["text"])

print()
print("=== ACTIONS ===")
for a in actions:
    print("[", a["confidence"], "]", a["speaker"], ":", a["text"])