from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from topics import decouper_en_sujets, trouver_mots_cles
from summary import resumer_sujet

with open("data/reunion2.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)

prenoms = []
for prise in prises:
    nom = prise["speaker"].lower()
    if nom not in prenoms:
        prenoms.append(nom)

sujets = decouper_en_sujets(phrases)
mots_cles = trouver_mots_cles(sujets, prenoms)

for i in range(len(sujets)):
    print("=== Sujet", i + 1, ":", ", ".join(mots_cles[i]), "===")
    print(resumer_sujet(sujets[i]))
    print()