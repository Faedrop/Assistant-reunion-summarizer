from cleaning import nettoyer_transcript
from segmentation import decouper_en_phrases

with open("data/reunion1.txt", encoding="utf-8") as f:
    texte_brut = f.read()

prises = nettoyer_transcript(texte_brut)
phrases = decouper_en_phrases(prises)

print(len(prises), "prises de parole ->", len(phrases), "phrases")
print()

for p in phrases:
    print(p["id"], "|", p["speaker"], "|", p["text"])