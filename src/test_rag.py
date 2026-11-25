from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases
from rag import construire_index, repondre

with open("data/reunion2.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)
index = construire_index(phrases)

questions = [
    "Qui doit contacter les fournisseurs ?",
    "Quelle est la nouvelle date de sortie ?",
    "Quel est le budget maximum pour les tests ?",
    "Quand a lieu la prochaine réunion ?",
    "Qui s'occupe du plan de test ?",
    "Qui a parlé du recrutement ?",
]

for q in questions:
    reponse, extraits = repondre(q, index, phrases)
    print("Q :", q)
    print("R :", reponse)
    print("   sources :")
    for e in extraits:
        print("     [" + e["time"] + "]", e["speaker"], ":", e["text"])
    print()